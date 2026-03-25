"""
Tests for the sunbather package
"""
import os
import pytest


def f():
    raise SystemExit(1)


def test_import():
    """
    Tests if sunbather can be imported.
    """
    try:
        import sunbather
    except ImportError:
        f()


def test_projectdirs():
    """
    Make sure projectpath exists
    """
    from sunbather import tools
    projectpath = tools.get_sunbather_project_path()
    assert os.path.isdir(
        projectpath
    ), "Please create the projectpath folder on your machine"


def test_planetstxt():
    """
    Make sure the planets.txt file exists
    """
    from sunbather import tools
    projectpath = tools.get_sunbather_project_path()    
    assert os.path.isfile(
        projectpath + "/planets.txt"
    ), "Please make sure the 'planets.txt' file is present in $SUNBATHER_PROJECT_PATH"


def test_seds():
    """
    Make sure the SED we need for this test has been copied to Cloudy
    """
    from sunbather import tools
    assert os.path.isfile(
        tools.get_cloudy_path() + "/data/SED/eps_Eri_binned.spec"
    ), (
        "Please copy /sunbather/stellar_SEDs/eps_Eri_binned.spec "
        "into $CLOUDY_PATH/data/SED/"
    )


def test_process_save_sp_excludes_turned_off_elements():
    """
    Species whose parent element is turned off should not be saved.
    """
    from sunbather import tools, convergeT_parker

    zdict = tools.get_zdict(z=0.0)
    save_sp = convergeT_parker.process_save_sp(["H", "He", "Li", "Li+", "Mg+2"], zdict)

    assert save_sp == ["H", "He"]


def test_process_save_sp_all_excludes_zero_abundance_elements():
    """
    Passing save_sp='all' should skip elements with zero abundance.
    """
    from sunbather import tools, convergeT_parker

    zdict = tools.get_zdict(z=1.0, zelem={"Li": 0.0})
    save_sp = convergeT_parker.process_save_sp("all", zdict, max_ion=2)

    assert "Li" not in save_sp
    assert "Li+" not in save_sp
    assert "He" in save_sp
