param(
    [switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$ProgressPreference = "SilentlyContinue"

$AppDirectory = Split-Path `
    -Parent `
    $MyInvocation.MyCommand.Path

$Root = [System.IO.Path]::GetFullPath(
    (Join-Path $AppDirectory "..")
)

$ControlApp = [System.IO.Path]::GetFullPath(
    (
        Join-Path `
            $AppDirectory `
            "control_center_app.py"
    )
)

$LogDirectory = Join-Path `
    $Root `
    "logs"

$LogPath = Join-Path `
    $LogDirectory `
    "controlcenter_launcher.log"

$ProcessNeedle = [regex]::Escape(
    $ControlApp
)


function Write-LauncherLog {
    param(
        [string]$Message
    )

    try {
        New-Item `
            -ItemType Directory `
            -Path $LogDirectory `
            -Force |
            Out-Null

        $Timestamp = (
            Get-Date
        ).ToString("o")

        Add-Content `
            -LiteralPath $LogPath `
            -Value "$Timestamp $Message" `
            -Encoding UTF8
    }
    catch {
    }
}


function Get-ControlCenterProcesses {
    Get-CimInstance Win32_Process |
        Where-Object {
            $Name = [string]$_.Name
            $CommandLine = [string]$_.CommandLine

            $IsPython = (
                $Name -ieq "python.exe" -or
                $Name -ieq "pythonw.exe"
            )

            $IsControlCenter = (
                -not [string]::IsNullOrWhiteSpace(
                    $CommandLine
                ) -and
                $CommandLine -match $ProcessNeedle
            )

            $IsPython -and
            $IsControlCenter
        }
}


if (-not (
    Test-Path `
        -LiteralPath $ControlApp `
        -PathType Leaf
)) {
    throw (
        "control_center_app.py not found: " +
        $ControlApp
    )
}


$PythonwCommand = Get-Command `
    pythonw.exe `
    -ErrorAction SilentlyContinue

if ($null -ne $PythonwCommand) {
    $Pythonw = (
        $PythonwCommand.Source
    )
}
else {
    $PythonCommand = Get-Command `
        python.exe `
        -ErrorAction Stop

    $Pythonw = (
        $PythonCommand.Source
    )
}


if ($ValidateOnly) {
    $Current = @(
        Get-ControlCenterProcesses
    )

    Write-Output (
        "CONTROL_CENTER_LAUNCHER_" +
        "VALIDATE_OK=1"
    )

    Write-Output (
        "CONTROL_CENTER_PROCESS_COUNT=" +
        $Current.Count
    )

    Write-Output (
        "PYTHON_EXECUTABLE=" +
        $Pythonw
    )

    Write-Output "RUNTIME_MUTATIONS=0"
    exit 0
}


$CreatedNew = $false

$Mutex = [System.Threading.Mutex]::new(
    $true,
    (
        "Local\AI_Bridge_Local_" +
        "Control_Center_Bat_" +
        "Launcher_0585"
    ),
    [ref]$CreatedNew
)

if (-not $CreatedNew) {
    Write-LauncherLog (
        "launcher_already_running=1"
    )

    $Mutex.Dispose()
    exit 0
}


try {
    $Existing = @(
        Get-ControlCenterProcesses
    )

    Write-LauncherLog (
        "existing_control_center_count=" +
        $Existing.Count
    )

    foreach (
        $ProcessInfo in $Existing
    ) {
        Write-LauncherLog (
            "stopping_control_center_pid=" +
            $ProcessInfo.ProcessId
        )

        Stop-Process `
            -Id (
                [int]$ProcessInfo.ProcessId
            ) `
            -Force `
            -ErrorAction Stop
    }


    $StopDeadline = (
        Get-Date
    ).AddSeconds(12)

    $Remaining = @()

    do {
        $Remaining = @(
            Get-ControlCenterProcesses
        )

        if (
            $Remaining.Count -eq 0
        ) {
            break
        }

        Start-Sleep `
            -Milliseconds 250
    }
    while (
        (Get-Date) -lt
        $StopDeadline
    )


    if (
        $Remaining.Count -ne 0
    ) {
        throw (
            "stale Control Center process " +
            "remains; count=" +
            $Remaining.Count
        )
    }


    $Arguments = @(
        "-X",
        "utf8",
        ('"{0}"' -f $ControlApp)
    )


    $Started = Start-Process `
        -FilePath $Pythonw `
        -ArgumentList $Arguments `
        -WorkingDirectory $Root `
        -PassThru


    Write-LauncherLog (
        "started_control_center_pid=" +
        $Started.Id
    )


    $StartDeadline = (
        Get-Date
    ).AddSeconds(20)

    $Current = @()

    do {
        $Current = @(
            Get-ControlCenterProcesses
        )

        if (
            $Current.Count -eq 1
        ) {
            break
        }

        if (
            $Current.Count -gt 1
        ) {
            throw (
                "more than one Control Center " +
                "process started; count=" +
                $Current.Count
            )
        }

        Start-Sleep `
            -Milliseconds 300
    }
    while (
        (Get-Date) -lt
        $StartDeadline
    )


    if (
        $Current.Count -ne 1
    ) {
        throw (
            "Control Center did not start " +
            "exactly once; count=" +
            $Current.Count
        )
    }


    Write-LauncherLog (
        "launcher_complete=1 pid=" +
        $Current[0].ProcessId
    )
}
catch {
    Write-LauncherLog (
        "launcher_error=" +
        $_.Exception.Message
    )

    throw
}
finally {
    try {
        $Mutex.ReleaseMutex()
    }
    catch {
    }

    $Mutex.Dispose()
}
