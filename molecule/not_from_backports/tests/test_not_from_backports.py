"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["nmap"])
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    assert host.package(pkg).is_installed
    # Verify that the version from Debian Backports is NOT installed
    if host.system_info.distribution == "debian":
        if host.system_info.codename == "bullseye":
            assert host.package(pkg).version.startswith("7.91")
        if host.system_info.codename == "bookworm":
            assert host.package(pkg).version.startswith("7.93")
