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
    reqsize: number;
    uaclass: string;
    actions: string;
    activity: string;
    anomaly?: boolean;
    confidence_score?: string;
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
    { name: "Anomaly", selector: row => row.anomaly ? "Yes" : "No", sortable: true, cell: row => <span style={{ color: row.anomaly ? 'red' : 'green' }}>{row.anomaly ? "Yes" : "No"}</span> },
    { name: "Confidence Score", selector: row => row.confidence_score || "N/A", sortable: true, cell: row => <span style={{ color: row.confidence_score ? 'blue' : 'gray' }}>{row.confidence_score || "N/A"}</span> },
    { name: "Threat Severity", selector: row => row.severity, sortable: true, sortFunction: (a, b) => severityOrder[a.severity] - severityOrder[b.severity] },
    { name: "User", selector: row => row.user, sortable: true },
    { name: "Method", selector: row => row.method, sortable: true },
    { name: "Req Size(Bytes)", selector: row => row.reqsize.toString(), sortable: true },
    { name: "Client Type", selector: row => row.uaclass, sortable: true },
    { name: "Response", selector: row => row.response_code, sortable: true },
    { name: "Actions", selector: row => row.actions, sortable: true },
    { name: "Activity", selector: row => row.activity, sortable: true },
    { name: "IP", selector: row => row.ip_address, sortable: true },
    { name: "URL", selector: row => row.url, sortable: true },
    { name: "Country", selector: row => row.country, sortable: true },
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
