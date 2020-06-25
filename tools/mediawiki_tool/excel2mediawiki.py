#!/usr/bin/env python3

from openpyxl import load_workbook
import sys
import os
import logging
import argparse

"""convert excel to mediawiki table format"""

logger = logging.getLogger('excel2mediawiki')


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
            result = "".join(self.escape_table.get(c, c) for c in str(self.content))
            result = result.replace("\n", "<br>")
            # if col content is '', cell show width and height will be small
            if result.strip() == '':
                result = "<br>"

        # add rowspan and colspan
        row_col_span_str = ''
        if self.rowspan > 1 or self.colspan > 1:
            if self.rowspan > 1:
                row_col_span_str = "rowspan=\"%d\"" % self.rowspan
            if self.colspan > 1:
                if row_col_span_str == '':
                    row_col_span_str = "colspan=\"%d\"" % self.colspan
                else:
                    row_col_span_str += " colspan=\"%d\"" % self.colspan
            row_col_span_str = "%s|" % row_col_span_str

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

    def get_tables_from_excel(self, excel_file_path, sheet_names=None):
        result_tables = {}
        wb = load_workbook(filename=excel_file_path)
        all_sheet_names = wb.get_sheet_names()
        result_tables_name = []
        if sheet_names is not None:
            for s in sheet_names:
                if s not in all_sheet_names:
                    logger.error(
                        "not find sheet in file, sheet name is %s, \
file is %s" % (s, excel_file_path))
                else:
                    result_tables_name.append(s)
        else:
            result_tables_name = all_sheet_names

        for s in result_tables_name:
            ws = wb[s]
            # get merged cell info
            all_merged_cell = ws.merged_cell_ranges
            merged_cell_map = {}
            for m in all_merged_cell:
                merged_cell_map["%d-%d" % (m.min_row - 1, m.min_col - 1)] = (m.size["rows"], m.size["columns"])
            table = []
            for r in ws.rows:
                table.append([c for c in r])
            # trans table to cell table
            cell_table = []
            for row_index in range(0, len(table)):
                rows = []
                for col_index in range(0, len(table[row_index])):
                    row_span, col_span = merged_cell_map.get("%d-%d" % (row_index, col_index), (1, 1))
                    if row_span > 1 or col_span > 1:
                        # this cell is in merged cell start positon<left top>
                        rows.append(Cell(table[row_index][col_index].value, row_span, col_span))
                    else:
                        # check is this cell in merged range
                        is_in_merged_range = False
                        for pos, r_c_range in merged_cell_map.items():
                            r, c = pos.split('-')
                            r = int(r)
                            c = int(c)
                            rows_length, cols_length = r_c_range
                            if row_index in range(r, r + rows_length) and \
                                col_index in range(c, c + cols_length):
                                is_in_merged_range = True
                                break
                        
                            logger.debug("check %d %d, range start pos %d %d,\
r_l, c_l: %d %d, is in: %s" % (row_index, col_index, r, c, rows_length, cols_length, is_in_merged_range))
                        if table[row_index][col_index].value is None:
                            if is_in_merged_range is True:
                                rows.append(None)
                            else:
                                rows.append(Cell('', row_span, col_span))
                        else:
                            rows.append(Cell(table[row_index][col_index].value,
                            row_span, col_span))
                cell_table.append(rows)

            result_tables[s] = cell_table

        return result_tables

    def write_cell_table_to_mediatext(self, cell_table, txt_file_name):
        with open(txt_file_name, 'w') as f:
            f.write("%s\n" % self.table_start_str)
            is_row_start = True
            for row in cell_table:
                if is_row_start is False:
                    f.write("%s\n" % self.row_split_str)
                else:
                    is_row_start = False
                f.write(self.col_start_str)
                is_col_start = True
                for col in row:
                    if col is not None:
                        if  is_col_start is True:
                            col_content = col.get_cell_wiki_content()
                            f.write(col_content)
                            is_col_start = False
                        else:
                            f.write("%s%s" % (
                                self.col_split_str,
                                col.get_cell_wiki_content()))
                f.write("\n")

            f.write("%s\n" % self.table_end_str)


def main(args):
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    table = Table()
    excel_file_path = args.excelfile
    if not os.path.exists(excel_file_path):
        logger.error("file not find, file path is %s" % excel_file_path)
        sys.exit(1)

    sheet_names = None
    if args.sheet is not None:
        sheet_names = [s.strip() for s in args.sheet.split(',')]
    tables = table.get_tables_from_excel(excel_file_path,
        sheet_names=sheet_names)
    logger.debug(str(tables))
    for tablename, cell_table in tables.items():
        logger.debug(str(cell_table))
        table.write_cell_table_to_mediatext(
            cell_table,
            os.path.join(args.outdir, "%s_%s.txt" % (
                excel_file_path.replace('.xlsx', ''), '_'.join(tablename.split()))
            )
        )

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="convert excel content to mediawiki table content")
    parse.add_argument('excelfile', help="excel file path")
    parse.add_argument('-s', '--sheet', help="sheet names split by comma, sheet to use, if not set this, all sheet use")
    parse.add_argument('-d', '--outdir', help="convert file in this dir", default="out")
    parse.add_argument("--debug", action="store_true", help="debug mode")
    args = parse.parse_args()
    log_level = logging.INFO
    if args.debug is True:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)
    main(args)
