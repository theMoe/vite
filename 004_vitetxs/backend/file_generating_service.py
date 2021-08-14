import pandas
from io import StringIO

def generate_return_file_msg(dictData):
    data_df = pandas.DataFrame(dictData)
    generated_file = __generate_csv_file(data_df)
    return {'file': generated_file, 'count': len(dictData)}


def __generate_csv_file(file_df):
    # Create an o/p buffer
    file_buffer = StringIO()
    # Write the dataframe to the buffer
    file_df.to_csv(file_buffer, encoding='utf-8', index=False, sep=',')
    # Seek to the beginning of the stream
    file_buffer.seek(0)
    return file_buffer