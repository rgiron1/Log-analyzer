import React from 'react';
import SummaryTable from './summaryTable';

type Props = {
    summary: any;
};

const AnalysisSummary: React.FC<Props> = ({ summary }) => {
    return (
        <div>
            <h2>Analysis Summary</h2>
            <p>Total entries: {summary.total_entries}</p>
            <p>High risk entries: {summary.high_risk_count}</p>
            <p>Critical risk entries: {summary.critical_risk_count}</p>

            <SummaryTable data={summary.timeline} />
        </div>
    );
};

export default AnalysisSummary;
