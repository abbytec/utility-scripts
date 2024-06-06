# Deshabilitar servicios innecesarios
$services = @("DiagTrack", "WSearch", "SysMain", "RetailDemo")
foreach ($service in $services) {
    Stop-Service -Name $service -Force
    Set-Service -Name $service -StartupType Disabled
}

# Optimizar la configuración de energía
powercfg -change standby-timeout-ac 0
powercfg -change standby-timeout-dc 0
powercfg -change monitor-timeout-ac 0
powercfg -change monitor-timeout-dc 0
powercfg -change disk-timeout-ac 0
powercfg -change disk-timeout-dc 0
powercfg -setactive SCHEME_MIN

# Ajustar la prioridad del proceso de PowerShell
$process = Get-Process -Id $PID
$process.PriorityClass = "High"

# Mejorar el rendimiento del sistema ajustando el planificador de tareas
reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 0x26 /f

# Configuración de red para mejorar la latencia
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TcpWindowSize /t REG_DWORD /d 0xFFFFFF /f

