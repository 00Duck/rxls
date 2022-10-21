import pandas as pd
import requests, json
import sys, os
from .servicenow_connector import ServiceNowConnector

class ExcelTestCaseProcessor:
    def __init__(self, input_path, output_path, env, range):
        self.excel_path = os.path.join(os.path.dirname(os.path.curdir), input_path)
        self.output_path = os.path.join(os.path.dirname(os.path.curdir), output_path or 'output.xlsx')
        self.output_df = pd.DataFrame()
        self.env = env
        self.range = range

    # Call this to run the test
    def process(self):
        conn = ServiceNowConnector(self.env)
        data_list = self.getDictFromExcel()
        self.printProgress(0, len(data_list))
        for inx, row in enumerate(data_list):
            resp = conn.call(row)
            resp_dict = self.formatRespDict(row, resp) # result will be something we can properly spit out to excel
            self.mergeResponseToOutput(resp_dict)
            self.printProgress(inx + 1, len(data_list))

        self.output_df.index = range(1, len(self.output_df) + 1) # Increment index by 1 to match test case numbers
        self.output_df.to_excel(self.output_path)
        print('Saved responses to ' + self.output_path)

    # Reads the Excel for data and returns a list of dicts
    def getDictFromExcel(self) -> list[dict]:
        try:
            # keep_default_na set to False with no na values means no strings will be parsed as NaN
            if self.range != None:
                # Skip rows keeps the header and skips up to the index
                df = pd.read_excel(self.excel_path, keep_default_na=False, skiprows=range(1, self.range[0]), nrows=self.range[1])
            else:
                df = pd.read_excel(self.excel_path, keep_default_na=False)
            df = df.convert_dtypes() # convert dtypes to string types
            df = df.applymap(str) # also needed to ensure Int fields (and others) are properly cast to string
            # Remove newlines from column headers if they exist
            df.rename(columns=lambda x: x.replace("\n", ""), inplace=True)
            return df.to_dict(orient='records')
        except Exception as err:
            print(str(err))
            sys.exit()
    # Creates the "Response" column using the response from SN
    def formatRespDict(self, row: dict, resp: requests.Response) -> dict:
        resp_dict = json.loads(resp.text)
        resp_partial = {
            "response": f"{resp.status_code}\n" + "\n".join([str(item[0]) + ": " + str(item[1]) for item in resp_dict.items()])
        }
        return resp_partial | row

    # Merges the response column with the original set of rows to view test data next to resp
    def mergeResponseToOutput(self, resp_dict: dict) -> None:
        row_df = pd.DataFrame(resp_dict,  index=[0])
        row_df = row_df.applymap(str) # Convert all values to strings!
        self.output_df = pd.concat([self.output_df, row_df], ignore_index=True)
    
    def printProgress(self, iteration, total):
        length = 50 # character length of bar
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        print(f'\rProgress: |{bar}| {percent}% Complete', end = "\r")
        if iteration == total: 
            print() # new line on complete