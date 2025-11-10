import re
import os
import boto3
import subprocess
import json
from urllib.parse import quote

# --- CONFIGURACIÓN DE AUTENTICACIÓN ---
# ... (sin cambios) ...
# 3. AWS CLI: El script ahora buscará el perfil 'sbws-users' por defecto.
#    Asegúrate de haber ejecutado 'aws sso login --profile sbws-users'
#    si tus credenciales han expirado.
# -----------------------------------------------------------------

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
        
    # AWS CodeCommit: https://sa-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name/pull-requests/789
    # Modificación para aceptar URLs de 'details', 'commits', 'changes' etc.
    codecommit_match = re.search(r'https://([^/]+)\.console\.aws\.amazon\.com/codesuite/codecommit/repositories/([^/]+)/pull-requests/(\d+)', pr_url)
    if codecommit_match:
        region, repo_name, pr_id = codecommit_match.groups()
        # Pasamos la región detectada a la función
        return _get_codecommit_pr(region, repo_name, pr_id)
        
    raise ValueError(f"URL de PR no reconocida: {pr_url}")

# -----------------------------------------------------------------
# --- SECCIÓN DE DATOS DE PRUEBA (MOCK) ---
# ... (sin cambios) ...
# -----------------------------------------------------------------

def _get_mock_data(pr_url):
    """
    Devuelve datos falsos pero con la estructura correcta para probar main.py
    """
    # ... (código de mock abreviado) ...
    pass


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

    profile_name = os.environ.get('AWS_PROFILE', 'sbws-users')
    print(f"    (Usando perfil de AWS: {profile_name})")

    try:
        session = boto3.Session(profile_name=profile_name)
        client = session.client('codecommit', region_name=region)

        # 1. Obtener información del PR
        pr_info = client.get_pull_request(pullRequestId=pr_id)
        target = pr_info['pullRequest']['pullRequestTargets'][0]

        repo_name = target['repositoryName']
        source_commit_id = target['sourceCommit']
        dest_commit_id = target['destinationCommit']

        print(f"    (Comparando {source_commit_id[:7]} contra {dest_commit_id[:7]})")

        # --- ARCHIVOS MODIFICADOS ---
        files = []
        diff_kwargs = {
            "repositoryName": repo_name,
            "beforeCommitSpecifier": dest_commit_id,
            "afterCommitSpecifier": source_commit_id
        }
        while True:
            page = client.get_differences(**diff_kwargs)
            for d in page.get('differences', []):
                if 'afterBlob' in d and 'path' in d['afterBlob']:
                    files.append(d['afterBlob']['path'])
            if 'nextToken' in page:
                diff_kwargs['nextToken'] = page['nextToken']
            else:
                break

        # --- COMMITS ---
        # CodeCommit no tiene endpoint para listar commits entre dos commits.
        # Tomamos solo el commit de origen y destino como referencia.
        commits = []
        for commit_id in [dest_commit_id, source_commit_id]:
            commit_data = client.get_commit(repositoryName=repo_name, commitId=commit_id)
            commits.append({
                "sha": commit_data['commit']['commitId'],
                "message": commit_data['commit']['message']
            })

        return {
            "repo_name": repo_name,
            "files": files,
            "commits": commits
        }

    except Exception as e:
        print(f"  Error procesando CodeCommit PR {pr_id} en {repo_name_from_url}: {e}")
        if 'ExpiredToken' in str(e) or 'credentials' in str(e):
            print(f"  --> PARECE UN ERROR DE CREDENCIALES. Asegúrate de haber ejecutado: 'aws sso login --profile {profile_name}'")
        raise

