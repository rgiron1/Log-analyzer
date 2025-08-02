import React, { useState, useMemo } from "react";

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

const severityOrder = ["Critical", "High", "Medium", "Low", "None"];

type Props = {
    data: timeLineEntry[];
};

type SortConfig = {
    key: keyof timeLineEntry;
    direction: "ascending" | "descending";
};

const SummaryTable: React.FC<Props> = ({ data }) => {
    // State to track sorting column and direction
    const [sortConfig, setSortConfig] = useState<SortConfig | null>(null);

    // Memoized sorted data to avoid unnecessary sorting on every render
    const sortedData = useMemo(() => {
        if (!sortConfig) return data;

        const sorted = [...data].sort((a, b) => {
            //Sort by severity by severity order
            if (sortConfig.key === "severity") {
                const aIdx = severityOrder.indexOf(a.severity);
                const bIdx = severityOrder.indexOf(b.severity);
                return (aIdx - bIdx) * (sortConfig.direction === "ascending" ? 1 : -1);
            }

            const aVal = a[sortConfig.key];
            const bVal = b[sortConfig.key];

            // Numeric sort for request_size, else string localeCompare
            if (
                typeof aVal === "number" &&
                typeof bVal === "number"
            ) {
                return (
                    (aVal - bVal) * (sortConfig.direction === "ascending" ? 1 : -1)
                );
            }

            // For string values
            return (
                aVal.toString().localeCompare(bVal.toString(), undefined, {
                    numeric: true,
                    sensitivity: "base",
                }) * (sortConfig.direction === "ascending" ? 1 : -1)
            );
        });

        return sorted;
    }, [data, sortConfig]);

    // Set state for sorting configuration via toggle
    const requestSort = (key: keyof timeLineEntry) => {
        if (
            sortConfig &&
            sortConfig.key === key &&
            sortConfig.direction === "ascending"
        ) {
            setSortConfig({ key, direction: "descending" });
        } else {
            setSortConfig({ key, direction: "ascending" });
        }
    };

    // Helper functions to get class names and arrows for sorting
    const getClassNamesFor = (name: keyof timeLineEntry) => {
        if (!sortConfig) return;
        return sortConfig.key === name ? sortConfig.direction : undefined;
    };

    //show arrows for sorting
    const getArrowFor = (name: keyof timeLineEntry) => {
        if (!sortConfig) return "▲▼";
        if (sortConfig.key === name) {
            return sortConfig.direction === "ascending" ? "▲" : "▼";
        }
        return "▲▼";
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '100%', boxSizing: 'border-box' }}>
            <div className="table-container">
                <table className="timeline-table">
                    <thead>
                        <tr>
                            <th
                                onClick={() => requestSort("timestamp")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("timestamp")}
                                title="Sort by Timestamp"
                            >
                                Timestamp {getArrowFor("timestamp")}
                            </th>
                            <th
                                onClick={() => requestSort("severity")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("severity")}
                                title="Sort by Severity"
                            >
                                Severity {getArrowFor("severity")}
                            </th>
                            <th
                                onClick={() => requestSort("user")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("user")}
                                title="Sort by User"
                            >
                                User {getArrowFor("user")}
                            </th>
                            <th
                                onClick={() => requestSort("url")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("url")}
                                title="Sort by URL"
                            >
                                URL {getArrowFor("url")}
                            </th>
                            <th
                                onClick={() => requestSort("country")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("country")}
                                title="Sort by Country"
                            >
                                Country {getArrowFor("country")}
                            </th>
                            <th
                                onClick={() => requestSort("method")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("method")}
                                title="Sort by Method"
                            >
                                Method {getArrowFor("method")}
                            </th>
                            <th
                                onClick={() => requestSort("response_code")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("response_code")}
                                title="Sort by Response"
                            >
                                Response {getArrowFor("response_code")}
                            </th>
                            <th
                                onClick={() => requestSort("ip_address")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("ip_address")}
                                title="Sort by IP"
                            >
                                IP {getArrowFor("ip_address")}
                            </th>
                            <th
                                onClick={() => requestSort("request_size")}
                                style={{ cursor: "pointer" }}
                                className={getClassNamesFor("request_size")}
                                title="Sort by Req Size"
                            >
                                Req Size {getArrowFor("request_size")}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((event, idx) => (
                            <tr key={idx}>
                                <td>{event.timestamp}</td>
                                <td>{event.severity}</td>
                                <td>{event.user}</td>
                                <td>{event.url}</td>
                                <td>{event.country}</td>
                                <td>{event.method}</td>
                                <td>{event.response_code}</td>
                                <td>{event.ip_address}</td>
                                <td>{event.request_size}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div >
    );
};

export default SummaryTable;
