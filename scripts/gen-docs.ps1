#!/usr/bin/env pwsh
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ScriptDir 'gen-docs'

if (-not (Test-Path $ScriptPath)) {
    throw "Unable to locate companion script: $ScriptPath"
}

& bash $ScriptPath @Args
