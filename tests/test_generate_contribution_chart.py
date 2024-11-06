# test_generate_contribution_chart.py

import pytest
from unittest.mock import patch, MagicMock
import json
import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for tests
import matplotlib.pyplot as plt
import sys

# Ensure the script directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from generate_contribution_chart import generate_contribution_chart

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        yield mock_run

def test_generate_contribution_chart(mock_subprocess_run):
    # Mock the branches response
    mock_branches_response = MagicMock()
    mock_branches_response.returncode = 0
    mock_branches_response.stdout = json.dumps([
        {"name": "main"},
        {"name": "dev"}
    ])
    
    # Mock the commits response
    mock_commits_response_main = MagicMock()
    mock_commits_response_main.returncode = 0
    mock_commits_response_main.stdout = json.dumps([
        {"commit": {"author": {"name": "Alice"}}}
    ])
    
    mock_commits_response_dev = MagicMock()
    mock_commits_response_dev.returncode = 0
    mock_commits_response_dev.stdout = json.dumps([
        {"commit": {"author": {"name": "Bob"}}}
    ])
    
    # Set the side effects for the mock run method
    mock_subprocess_run.side_effect = [
        mock_branches_response,  # First call for branches
        mock_commits_response_main,  # First call for commits (main branch)
        mock_commits_response_dev  # Second call for commits (dev branch)
    ]
    
    # Call the function
    contributions = generate_contribution_chart()
    
    # Check the contributions dictionary
    expected_contributions = {"Alice": 1, "Bob": 1}
    assert contributions == expected_contributions

    # Check if the chart is generated
    assert os.path.exists("images/contribution_chart.png")

if __name__ == '__main__':
    pytest.main()