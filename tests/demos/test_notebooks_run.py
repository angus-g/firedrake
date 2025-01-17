import pytest
import os
import subprocess
import glob


cwd = os.path.abspath(os.path.dirname(__file__))
nb_dir = os.path.join(cwd, "..", "..", "docs", "notebooks")


# Discover the notebook files by globbing the notebook directory
@pytest.fixture(params=glob.glob(os.path.join(nb_dir, "*.ipynb")),
                ids=lambda x: os.path.basename(x))
def ipynb_file(request):
    if request.param.endswith("08-composable-solvers.ipynb"):
        pytest.xfail("FIX THIS LATER: Have to update our PETSc fork to fix build issues")
    return os.path.abspath(request.param)


@pytest.mark.skipcomplex  # Will need to add a seperate case for a complex tutorial.
def test_notebook_runs(ipynb_file, tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    pytest = os.path.join(os.environ.get("VIRTUAL_ENV"), "bin", "pytest")
    subprocess.check_call([pytest, "--nbval-lax", ipynb_file])
