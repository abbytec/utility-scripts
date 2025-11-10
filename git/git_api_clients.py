import re
import os
import boto3
import subprocess
import json
from urllib.parse import quote

# --- CONFIGURACIÓN DE AUTENTICACIÓN ---
# Este script ahora asume que has iniciado sesión a través de los CLI:
# 1. GitHub CLI: 'gh auth login'
# 2. GitLab CLI: 'glab auth login'
# 3. AWS CLI: 'aws configure' (usado por boto3)
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1") # Región por defecto si no está configurada

# -----------------------------------------------------------------
# --- MODO DE PRUEBA ---
# -----------------------------------------------------------------
# Cambia esto a True si quieres volver a los datos de prueba
USE_MOCK_DATA = False
# -----------------------------------------------------------------

def _run_cli_command(command_parts):
    """
    Helper para ejecutar comandos CLI y parsear su salida JSON.
    """
    try:
        # Ejecuta el comando
        result = subprocess.run(
            command_parts,
            capture_output=True,
            text=True,
            check=True,  # Lanza un error si el comando falla
            encoding='utf-8'
        )
        # Parsea la salida JSON
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {' '.join(command_parts)}")
        print(f"STDERR: {e.stderr}")
        raise
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar JSON del comando: {' '.join(command_parts)}")
        raise
    except FileNotFoundError:
        print(f"Error: El comando '{command_parts[0]}' no se encontró.")
        print("Asegúrate de que los CLI (gh, glab) estén instalados y en tu PATH.")
        raise


def get_pr_details(pr_url):
    """
    Función principal (Dispatcher).
    Identifica el proveedor y llama a la función correspondiente.
    """
    if USE_MOCK_DATA:
        print("    (Usando datos MOCK)")
        return _get_mock_data(pr_url)

    # --- Lógica de Parseo de URL ---
    
    # GitHub: https://github.com/owner/repo/pull/123
    github_match = re.search(r'github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_url)
    if github_match:
        owner, repo, pr_number = github_match.groups()
        return _get_github_pr(owner, repo, pr_number)
        
    # GitLab: https://gitlab.com/group/subgroup/repo/-/merge_requests/456
    gitlab_match = re.search(r'gitlab\.com/([^/]+(?:/[^/]+)*)/-/merge_requests/(\d+)', pr_url)
    if gitlab_match:
        # project_path puede ser 'group/repo' o 'group/subgroup/repo'
        project_path, mr_iid = gitlab_match.groups()
        return _get_gitlab_pr(project_path, mr_iid)
        
    # AWS CodeCommit: https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name/pull-requests/789
    codecommit_match = re.search(r'console\.aws\.amazon\.com/codesuite/codecommit/repositories/([^/]+)/pull-requests/(\d+)', pr_url)
    if codecommit_match:
        repo_name, pr_id = codecommit_match.groups()
        # Asumimos que la región está en la variable de entorno o es la por defecto
        return _get_codecommit_pr(AWS_REGION, repo_name, pr_id)
        
    raise ValueError(f"URL de PR no reconocida: {pr_url}")

# -----------------------------------------------------------------
# --- SECCIÓN DE DATOS DE PRUEBA (MOCK) ---
# (Se mantiene por si se necesita volver a probar)
# -----------------------------------------------------------------

def _get_mock_data(pr_url):
    """
    Devuelve datos falsos pero con la estructura correcta para probar main.py
    """
    if "github" in pr_url:
        return {
            "repo_name": "mi-repo-principal",
            "files": ["src/main.js", "apps/facturacion/factura.py", "apps/usuarios/perfil.js"],
            "commits": [
                {"sha": "a1b2c3d4e5f6", "message": "Feat: Agrega login de usuarios"},
                {"sha": "b2c3d4e5f6a1", "message": "Fix: Corrige cálculo de IVA en facturación"}
            ]
        }
    elif "gitlab" in pr_url:
        return {
            "repo_name": "proyecto-gitlab/backend",
            "files": ["README.md", "src/index.js"],
            "commits": [
                {"sha": "c3d4e5f6a1b2", "message": "Doc: Actualiza README"}
            ]
        }
    elif "codecommit" in pr_url:
        return {
            "repo_name": "aws-repo-legacy",
            "files": ["apps/usuarios/admin.java"],
            "commits": [
                {"sha": "d4e5f6a1b2c3", "message": "Refactor: Mueve lógica de admin"}
            ]
        }
    else:
        # Caso para el PR 4
        return {
            "repo_name": "mi-repo-principal",
            "files": ["apps/facturacion/reporte.py"],
            "commits": [
                {"sha": "e5f6a1b2c3d4", "message": "Feat: Nuevo reporte de ventas"}
            ]
        }

# -----------------------------------------------------------------
# --- IMPLEMENTACIONES DE API (REALES) ---
# -----------------------------------------------------------------

def _get_github_pr(owner, repo, pr_number):
    """
    Obtiene los detalles de un PR de GitHub usando el CLI 'gh'.
    """
    print(f"    (API real GitHub: {owner}/{repo} PR #{pr_number})")
    repo_path = f"{owner}/{repo}"
    
    # 1. Obtener archivos
    # 'gh api' maneja la paginación automáticamente
    files_endpoint = f"repos/{repo_path}/pulls/{pr_number}/files"
    files_data = _run_cli_command(["gh", "api", files_endpoint, "--paginate"])
    files = [f['filename'] for f in files_data]
    
    # 2. Obtener commits
    commits_endpoint = f"repos/{repo_path}/pulls/{pr_number}/commits"
    commits_data = _run_cli_command(["gh", "api", commits_endpoint, "--paginate"])
    commits = [
        {"sha": c['sha'], "message": c['commit']['message']}
        for c in commits_data
    ]
    
    return {
        "repo_name": repo_path,
        "files": files,
        "commits": commits
    }
    

def _get_gitlab_pr(project_path, mr_iid):
    """
    Obtiene los detalles de un MR de GitLab usando el CLI 'glab'.
    """
    print(f"    (API real GitLab: {project_path} MR !{mr_iid})")
    
    # El project_path (ej: 'grupo/repo') debe estar codificado para la URL
    encoded_path = quote(project_path, safe='')
    
    # 1. Obtener archivos (cambios)
    # 'glab api' maneja la paginación
    changes_endpoint = f"projects/{encoded_path}/merge_requests/{mr_iid}/changes"
    changes_data = _run_cli_command(["glab", "api", changes_endpoint])
    # GitLab anida los archivos bajo 'changes'
    files = [change['new_path'] for change in changes_data.get('changes', [])]
    
    # 2. Obtener commits
    commits_endpoint = f"projects/{encoded_path}/merge_requests/{mr_iid}/commits"
    commits_data = _run_cli_command(["glab", "api", commits_endpoint, "--paginate"])
    commits = [
        # GitLab usa 'id' para el SHA y 'title' para la primera línea
        {"sha": c['id'], "message": c['title']}
        for c in commits_data
    ]
    
    return {
        "repo_name": project_path,
        "files": files,
        "commits": commits
    }

def _get_codecommit_pr(region, repo_name_from_url, pr_id):
    """
    Obtiene los detalles de un PR de AWS CodeCommit usando boto3.
    """
    print(f"    (API real CodeCommit: {region}/{repo_name_from_url} PR {pr_id})")
    
    client = boto3.client('codecommit', region_name=region)
    
    try:
        # 1. Obtener información del PR para encontrar las referencias
        pr_info = client.get_pull_request(pullRequestId=pr_id)
        target = pr_info['pullRequest']['pullRequestTargets'][0]
        
        repo_name = target['repositoryName']
        source_ref = target['sourceReference']
        dest_ref = target['destinationReference']

        # 2. Obtener el 'merge base' (el ancestro común)
        # Esto nos da el punto de partida correcto para el diff y los commits
        source_commit_id = client.get_commit(repositoryName=repo_name, commitId=source_ref)['commit']['commitId']
        dest_commit_id = client.get_commit(repositoryName=repo_name, commitId=dest_ref)['commit']['commitId']

        merge_base_resp = client.get_merge_base(
            repositoryName=repo_name,
            sourceCommitSpecifier=source_commit_id,
            destinationCommitSpecifier=dest_commit_id
        )
        merge_base_id = merge_base_resp['mergeBaseCommitId']

        # 3. Obtener los commits entre el 'merge base' y el commit 'source'
        # Usamos un paginador para manejar más de 100 commits
        paginator_commits = client.get_paginator('get_commits')
        commits_pages = paginator_commits.paginate(
            repositoryName=repo_name,
            comparisonOperator='BETWEEN',
            fromCommitSpecifier=merge_base_id,
            toCommitSpecifier=source_commit_id
        )
        
        commits = []
        for page in commits_pages:
            for c in page['commits']:
                commits.append({"sha": c['commitId'], "message": c['message']})

        # 4. Obtener los archivos modificados
        paginator_diffs = client.get_paginator('get_differences')
        diff_pages = paginator_diffs.paginate(
            repositoryName=repo_name,
            beforeCommitSpecifier=merge_base_id,
            afterCommitSpecifier=source_commit_id
        )
        
        files = []
        for page in diff_pages:
            for d in page['differences']:
                if 'afterBlob' in d and 'path' in d['afterBlob']:
                    files.append(d['afterBlob']['path'])
        
        return {
            "repo_name": repo_name,
            "files": files,
            "commits": commits
        }

    except Exception as e:
        print(f"  Error procesando CodeCommit PR {pr_id} en {repo_name_from_url}: {e}")
        # Re-lanzamos el error para que main.py lo capture
        raise
