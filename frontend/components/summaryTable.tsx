import React from "react";
import DataTable, { TableColumn } from "react-data-table-component";

type timeLineEntry = {
    timestamp: string;
    severity: string;
    user: string;
    url: string;
    country: string;
    method: string;
    response_code: string;
    ip_address: string;
    request_size: number;
};


const severityOrder: { [key: string]: number } = {
    Critical: 1,
    High: 2,
    Medium: 3,
    Low: 4,
};


type Props = {
    data: timeLineEntry[];
};

const columns: TableColumn<timeLineEntry>[] = [
    { name: "Timestamp", selector: row => row.timestamp, sortable: true },
    { name: "Severity", selector: row => row.severity, sortable: true, sortFunction: (a, b) => severityOrder[a.severity] - severityOrder[b.severity] },
    { name: "User", selector: row => row.user, sortable: true },
    { name: "URL", selector: row => row.url, sortable: true },
    { name: "Country", selector: row => row.country, sortable: true },
    { name: "Method", selector: row => row.method, sortable: true },
    { name: "Response", selector: row => row.response_code, sortable: true },
    { name: "IP", selector: row => row.ip_address, sortable: true },
    { name: "Req Size(Bytes)", selector: row => row.request_size.toString(), sortable: true },
];

const SummaryTable: React.FC<Props> = ({ data }) => {
    return (
        <DataTable
            title="Timeline of Events"
            columns={columns}
            data={data}
            defaultSortFieldId="timestamp"
            pagination={true}
            highlightOnHover={true}
            striped={true}
            responsive={true}
        />
    );
};

export default SummaryTable;
