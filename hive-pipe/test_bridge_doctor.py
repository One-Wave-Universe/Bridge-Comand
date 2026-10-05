#!/usr/bin/env python3
import unittest
from unittest import mock

import bridge_doctor


class BridgeDoctorTests(unittest.TestCase):
    def test_exit_codes_distinguish_failure_from_unverified(self):
        self.assertEqual(bridge_doctor.overall_exit([
            {"status":"PASS"}
        ]), 0)
        self.assertEqual(bridge_doctor.overall_exit([
            {"status":"NOT_VERIFIED"}
        ]), 2)
        self.assertEqual(bridge_doctor.overall_exit([
            {"status":"FAIL"}
        ]), 1)

    def test_ci_static_contracts_pass_in_repository(self):
        checks = bridge_doctor.static_checks()
        failures = [check for check in checks if check["status"] == "FAIL"]
        self.assertEqual(failures, [], failures)

    def test_inactive_required_service_is_failure(self):
        completed = mock.Mock(returncode=3, stdout="inactive\n", stderr="")
        with mock.patch.object(bridge_doctor, "run", return_value=completed):
            check = bridge_doctor.service_or_process("example.service", "example")
        self.assertEqual(check["status"], "FAIL")
        self.assertIn("repair", check["action"].lower())

    def test_missing_science_checkout_is_unverified(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d, mock.patch.object(bridge_doctor,"SCIENCE",Path(d)/"missing"):
            checks=bridge_doctor.pull_checks()
        self.assertEqual(checks[0]["status"],"WARN")
        self.assertEqual(bridge_doctor.overall_exit(checks),2)

    def test_pull_installer_prepares_both_routes_and_external_work_root(self):
        installer = (bridge_doctor.HERE / "install_chatgpt_terminal_pull.sh").read_text()
        self.assertIn("chatgpt-terminal-backup", installer)
        self.assertIn("EXTERNAL_ROOT", installer)
        self.assertIn("$HERE/chatgpt_terminal_pull.py", installer)
        self.assertIn("$HERE/bridge_doctor.py", installer)

    def test_gateway_installer_resolves_canonical_bridge_root(self):
        installer = (bridge_doctor.HERE / "install_gateway.sh").read_text()
        self.assertIn('REPO_ROOT="$(dirname -- "$SCRIPT_DIR")"', installer)
        self.assertIn('PROJECT_ROOT="${ONE_WAVE_PROJECT_ROOT:-$REPO_ROOT}"', installer)


if __name__ == "__main__":
    unittest.main()
