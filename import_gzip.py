import gzip
import shutil

def unzip_file(input_filepath, output_filepath):
    with gzip.open(input_filepath, 'rb') as f_in:
        with open(output_filepath, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Specify the path to the gzipped file and the output file path
input_filepath = 'employees.sql.gz'
output_filepath = 'employees.sql'

unzip_file(input_filepath, output_filepath)
print(f"Unzipped file saved as {output_filepath}")