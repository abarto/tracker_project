import sys

from base64 import (b64encode, b64decode)
from java.io import ByteArrayOutputStream
from json import loads

from net.sf.dynamicreports.report.builder.DynamicReports import (
    cmp as dr_cmp, col as dr_col, report as dr_report, type as dr_type
)
from net.sf.dynamicreports.report.datasource import DRDataSource


def get_report_data(report_data):
    return loads(b64decode(report_data).decode("utf-8"))


def create_report(data_source):
    output_stream = ByteArrayOutputStream()
    dr_report() \
        .columns(
            dr_col.column('Pk', 'pk', dr_type.integerType()),
            dr_col.column('Name', 'name', dr_type.stringType()),
            dr_col.column('Description', 'description', dr_type.stringType()),
            dr_col.column('Severity', 'severity', dr_type.stringType()),
            dr_col.column('Closed', 'closed', dr_type.booleanType()),
            dr_col.column('Location', 'location', dr_type.stringType()),
            dr_col.column('Created', 'created', dr_type.stringType())
        ) \
        .title(dr_cmp.text('Incidents')) \
        .setDataSource(data_source) \
        .toPdf(output_stream)

    return output_stream.toByteArray()


def create_data_source(data):
    dr_data_source = DRDataSource(
        ['pk', 'name', 'description', 'severity', 'closed', 'location', 'created']
    )

    for incident in data:
        dr_data_source.add(
            incident['pk'],
            incident['fields']['name'],
            incident['fields']['description'],
            incident['fields']['severity'],
            incident['fields']['closed'],
            incident['fields']['location'],
            incident['fields']['created']
        )

    return dr_data_source

if __name__ == '__main__':
    data_source = create_data_source(get_report_data(sys.argv[1]))
    report_pdf = create_report(data_source)

    print b64encode(report_pdf)