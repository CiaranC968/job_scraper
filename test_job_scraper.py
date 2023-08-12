import os
import random
import string


def test_prevent_overwrite():
    from job_scrapper import prevent_overwrite
    filename = ''.join(random.choices(string.ascii_lowercase, k=20))
    file_path = os.path.join(os.getcwd(), f"{filename}.txt")
    with open(file_path, 'w') as f_obj:
        f_obj.write('test file for job scraper')
    expected_file_path_1 = os.path.join(os.getcwd(), f"{filename}_(1).txt")
    actual_file_path_1 = prevent_overwrite(file_path)
    assert actual_file_path_1 == expected_file_path_1
    with open(actual_file_path_1, 'w') as f_obj:
        f_obj.write('test file for job scraper')
    expected_file_path_2 = os.path.join(os.getcwd(), f"{filename}_(2).txt")
    actual_file_path_2 = prevent_overwrite(actual_file_path_1)
    assert actual_file_path_2 == expected_file_path_2
    os.remove(file_path)
    os.remove(actual_file_path_1)


if __name__ == '__main__':
    test_prevent_overwrite()