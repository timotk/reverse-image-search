import subprocess


def test_cli():
    result = subprocess.run(
        [
            "python",
            "reverse_image_search/cli.py",
            "images/hills-2836301_1920_thumbnail.jpg",
            "images/",
        ],
        capture_output=True,
    )
    assert result.returncode == 0
    output_lines = str(result.stdout).split("\\n")
    assert output_lines[0] == 'b"Finding similar images...'
    assert output_lines[1] == "- to: images/hills-2836301_1920_thumbnail.jpg"
    assert output_lines[2] == "- in: images"
    assert output_lines[3] == "- filetypes: ['.jpg', '.jpeg']"
    assert output_lines[4] == "- threshold: 0.9"
    assert output_lines[-5:-1] == [
        "filepath                                 similarity",
        "---------------------------------------  ------------",
        "images/hills-2836301_1920_thumbnail.jpg  100%",
        "images/hills-2836301_1920.jpg            99%",
    ]


def test_cli_no_matches_found():
    result = subprocess.run(
        [
            "python",
            "reverse_image_search/cli.py",
            "images/hills-2836301_1920_thumbnail.jpg",
            "reverse_image_search",
        ],
        capture_output=True,
    )
    assert result.returncode == 0
    output_lines = str(result.stdout).split("\\n")
    assert output_lines[0] == 'b"Finding similar images...'
    assert output_lines[1] == "- to: images/hills-2836301_1920_thumbnail.jpg"
    assert output_lines[2] == "- in: reverse_image_search"
    assert output_lines[3] == "- filetypes: ['.jpg', '.jpeg']"
    assert output_lines[4] == "- threshold: 0.9"
    assert "No matches found :(" in output_lines[-2]
