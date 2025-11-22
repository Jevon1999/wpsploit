#!/usr/bin/env python3
"""
Test Script untuk WP AutoExploit Tool
Fungsi: Testing workflow dan integration
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import Logger
from settings import Settings
from exploitdb_gitlab import ExploitDBGitlab
from exploit_parser import ExploitParser

def test_exploitdb_integration():
    """Test ExploitDB GitLab integration"""
    print("\n" + "="*60)
    print("TEST 1: ExploitDB GitLab Integration")
    print("="*60)
    
    logger = Logger()
    settings = Settings(logger)
    
    exploitdb = ExploitDBGitlab(
        logger,
        settings.get('exploitdb_gitlab.repo_url'),
        settings.get('exploitdb_gitlab.cache_dir')
    )
    
    # Test 1: Update repo
    print("\n[1] Testing repo update...")
    try:
        repo_path = exploitdb.update_repo()
        print(f"✓ Repo path: {repo_path}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 2: Parse exploits
    print("\n[2] Testing exploit parsing...")
    try:
        exploits = exploitdb.parse_exploits(repo_path)
        print(f"✓ Parsed {len(exploits)} WordPress exploits")
        if exploits:
            sample = exploits[0]
            print(f"  Sample: {sample['id']} - {sample.get('title', '')[:50]}")
            print(f"  CVEs: {sample.get('cves', [])}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 3: Search by CVE
    print("\n[3] Testing CVE search...")
    test_cves = ["CVE-2024-1071", "CVE-2023-6961", "CVE-2022-0215"]
    
    for cve in test_cves:
        results = exploitdb.get_exploits_by_cve(cve)
        if results:
            print(f"✓ {cve}: Found {len(results)} exploits")
            for r in results[:2]:
                print(f"    - {r['id']}: {r.get('title', '')[:60]}")
        else:
            print(f"  {cve}: No exploits found")
    
    return True

def test_exploit_parser():
    """Test exploit parser"""
    print("\n" + "="*60)
    print("TEST 2: Exploit Parser")
    print("="*60)
    
    logger = Logger()
    parser = ExploitParser(logger)
    
    # Test Python exploit
    python_code = """#!/usr/bin/env python3
# CVE-2024-1234 WordPress Plugin Exploit
# Author: Test
import requests
import sys

def exploit(url):
    print(f"Exploiting {url}")
    # Exploit code here
    
if __name__ == "__main__":
    target = sys.argv[1]
    exploit(target)
"""
    
    print("\n[1] Testing Python exploit parsing...")
    parsed = parser.parse_exploit_code(python_code)
    print(f"  CVEs: {parsed['cves']}")
    print(f"  Language: {parsed['language']}")
    print(f"  Is WordPress: {parsed['is_wordpress']}")
    print(f"  Description: {parsed['description'][:50] if parsed['description'] else 'N/A'}")
    
    # Test Bash exploit
    bash_code = """#!/bin/bash
# CVE-2023-5678 WordPress RCE
# Exploit for WordPress 5.x

TARGET=$1
curl -X POST "$TARGET/wp-admin/admin-ajax.php" -d "action=exploit"
"""
    
    print("\n[2] Testing Bash exploit parsing...")
    parsed = parser.parse_exploit_code(bash_code)
    print(f"  CVEs: {parsed['cves']}")
    print(f"  Language: {parsed['language']}")
    print(f"  Is WordPress: {parsed['is_wordpress']}")
    
    return True

def test_config():
    """Test configuration"""
    print("\n" + "="*60)
    print("TEST 3: Configuration")
    print("="*60)
    
    logger = Logger()
    settings = Settings(logger, "config.json")
    
    print("\n[1] Testing config loading...")
    print(f"  ExploitDB URL: {settings.get('exploitdb_gitlab.repo_url')}")
    print(f"  Cache dir: {settings.get('cache.cache_dir')}")
    print(f"  Auto update: {settings.get('exploitdb_gitlab.auto_update')}")
    print(f"  Exploit timeout: {settings.get('exploit.timeout_seconds')}")
    print(f"  Max retries: {settings.get('exploit.max_retries')}")
    
    return True

def test_workflow_simulation():
    """Simulate full workflow tanpa actual execution"""
    print("\n" + "="*60)
    print("TEST 4: Workflow Simulation")
    print("="*60)
    
    # Simulate Nuclei output
    mock_vulnerabilities = [
        {
            "template-id": "CVE-2024-1071",
            "info": {
                "name": "WordPress Plugin XYZ Vulnerability",
                "tags": ["cve", "cve-2024-1071", "wordpress"]
            }
        },
        {
            "template-id": "CVE-2023-6961",
            "info": {
                "name": "WordPress Core RCE",
                "tags": ["cve", "cve-2023-6961", "wordpress", "rce"]
            }
        }
    ]
    
    print("\n[1] Simulating Nuclei scan results...")
    print(f"  Found {len(mock_vulnerabilities)} vulnerabilities")
    
    logger = Logger()
    parser = ExploitParser(logger)
    
    print("\n[2] Extracting CVEs...")
    for vuln in mock_vulnerabilities:
        tags = vuln.get('info', {}).get('tags', [])
        cves = [tag for tag in tags if tag.upper().startswith('CVE-')]
        print(f"  ✓ {vuln['template-id']}: {cves}")
    
    print("\n[3] Workflow steps:")
    print("  1. ✓ Nuclei scan")
    print("  2. ✓ CVE extraction")
    print("  3. → ExploitDB matching (requires repo)")
    print("  4. → Exploit download")
    print("  5. → Parameter injection")
    print("  6. → Execution")
    
    return True

def main():
    print("\n" + "="*60)
    print("WP AUTOEXPLOIT TOOL - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Configuration", test_config),
        ("Exploit Parser", test_exploit_parser),
        ("Workflow Simulation", test_workflow_simulation),
        ("ExploitDB Integration", test_exploitdb_integration),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} FAILED: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)
    
    return all(r for _, r in results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
