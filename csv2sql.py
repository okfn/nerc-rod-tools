import sys
import csv

insert_statement = "INSERT INTO {table} ({columns}) VALUES ({values});"

def csv2sql(tablename, source):
    reader = csv.reader(source)
    columns = reader.next()

    col_str = ','.join(columns)
    row_str = insert_statement.format(table=tablename, columns=col_str, values="{values}")

    def sql_quote(str):
        return "\"%s\"" % str.replace('\"', '\"\"');

    print "BEGIN;"

    for row in reader:
        val_str = ','.join(map(sql_quote, row))
        print row_str.format(values=val_str)

    print "COMMIT;"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        tablename = sys.argv[1]
        csv2sql(tablename, sys.stdin)
    else:
        print "Usage: %s tablename < foo.csv > foo.sql" % sys.argv[0]
