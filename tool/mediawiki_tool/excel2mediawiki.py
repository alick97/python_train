#!/usr/bin/env python3

from openpyxl import load_workbook
import sys
import os

"""convert excel to mediawiki table format"""

def show_err(s):
    sys.stderr.write("error: %s\n" % s)

class Cell(object):
    """one cell of table"""
    def __init__(self, content=None, rowspan=1, colspan=1):
        self.content = content
        self.rowspan = rowspan
        self.colspan = colspan
        self.escape_table = {
            "&": "&amp;",
            "!": "<nowiki>!</nowiki>",
            "|": "<nowiki>|</nowiki>",
        }

    def get_cell_wiki_content(self):
        """return wiki content str"""
        # escape special mark
        result = ''
        if self.content is not None:
            result = "".join(self.escape_table.get(c, c) for c in self.content)
            result = result.replace("\n", "<br>")

        # add rowspan and colspan
        row_col_span_str = ''
        if  self.rowspan > 1 or self.colspan > 1:
            row_span_str = ''
            col_span_str = ''
            if self.rowspan > 1:
                row_span_str = "rowspan=\"%d\"" % self.rowspan
            if self.colspan > 1:
                col_span_str = "colspan=\"%d\"" % self.colspan
            row_col_span_str = "%s %s|" % (row_span_str, col_span_str)

        result = "%s%s" % (row_col_span_str, result)
        return result

    def __str__(self):
        return "cell content: %s, rowspan: %d, colspan: %d" % (
            self.content, self.rowspan, self.colspan)
    
    def __repr__(self):
        return "cell content: %s, rowspan: %d, colspan: %d\n" % (
            self.content, self.rowspan, self.colspan)


class Table(object):
    """one table by  two dimentional array"""
    def __init__(self):
        self.table_start_str = "{| class=\"wikitable\""
        self.table_end_str = "|}"
        self.row_split_str = "|-"
        self.col_start_str = "|"
        self.col_split_str = "||"

    def get_cell_row_and_col_span(self, table, row_index, col_index):
        """
        find row_span and col_span by table of two dimentional array
        param: row_index, row index of table
               col_index, col index of table
        return: (row_span<int>, (col_span)<int>)
        """
        table_rows = len(table)
        table_cols = 0 if table_rows == 0 else len(table[0])
        row_span = 1
        col_span = 1
        assert(row_index >= 0 and row_index < table_rows)
        assert(col_index >= 0 and col_index < table_cols)
        if table[row_index][col_index] is None:
            return 1, 1

        for r in range(row_index + 1, table_rows):
            if table[r][col_index] is None:
                row_span += 1
            else:
                break

        for c in range(col_index, table_cols):
            if table[row_index][c] is None:
                col_span += 1
            else:
                break

        return row_span, col_span

    def trans_table_to_cell_table(self, table):
        """
        trans table to cell table
        param: table is two dimentional array
               [
                   [str, str, None, ...],
                   [...]
               ]
        return: two dimentional array, element
                is class cell 
        """
        result = []
        table_rows = len(table)
        table_cols = 0 if table_rows == 0 else len(table[0])
        for row_index in range(0, table_rows):
            row_cells = []
            for col_index in range(0, table_cols):
                if table[row_index][col_index] is None:
                    row_cells.append(None)
                else:
                    # check is this cell combined
                    row_span, col_span = self.get_cell_row_and_col_span(
                        table, row_index, col_index)
                    row_cells.append(Cell(
                        content=str(table[row_index][col_index]),
                        rowspan=row_span,
                        colspan=col_span
                    ))
            result.append(row_cells)

        return result

    def get_tables_from_excel(self, excel_file_path, sheet_names=None):
        result_tables = {}
        wb = load_workbook(filename=excel_file_path, read_only=True)
        all_sheet_names = wb.get_sheet_names()
        result_tables_name = []
        if sheet_names is not None:
            for s in sheet_names:
                if s not in all_sheet_names:
                    show_err("not find sheet in file, sheet name is %s, file is %s"
                    % (s, excel_file_path))
                else:
                    result_tables_name.append(s)
        else:
            result_tables_name = all_sheet_names
        
        for s in result_tables_name:
            ws = wb[s]
            table = []
            for r in ws.rows:
                table.append([c.value for c in r])
                result_tables[s] = table

        return result_tables
    
    def write_cell_table_to_mediatext(self, cell_table, txt_file_name):
        with open(txt_file_name, 'w') as f:
            f.write("%s\n" % self.table_start_str)
            is_row_start=True
            for row in cell_table:
                if is_row_start == False:
                    f.write("%s\n" % self.row_split_str)
                else:
                    is_row_start = False
                f.write(self.col_start_str)
                is_col_start=True
                for col in row:
                    if col is not None:
                        if  is_col_start == True:
                            f.write(col.get_cell_wiki_content())
                            is_col_start=False
                        else:
                            f.write("%s%s" % (
                                self.col_split_str,
                                col.get_cell_wiki_content()))
                f.write("\n")

            print('write done')
            f.write("%s\n" % self.table_end_str)


if __name__ == '__main__':
    table = Table()
    excel_file_path='t.xlsx'
    tables = table.get_tables_from_excel(excel_file_path)
    print(tables)
    for tablename, t in tables.items():
        cell_table = table.trans_table_to_cell_table(t)
        print(cell_table)
        table.write_cell_table_to_mediatext(
            cell_table, "%s_%s.txt" % (
                excel_file_path.replace('.xlsx',''), '_'.join(tablename.split())
            )
        )