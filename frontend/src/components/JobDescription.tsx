interface JobDescriptionProps {
  value: string;
  onChange: (value: string) => void;
}

const JobDescription = ({ value, onChange }: JobDescriptionProps) => {
  return (
    <div className="rounded-xl border border-border bg-card p-6 card-elevated">
      <h2 className="text-lg font-semibold font-heading text-card-foreground mb-4">
        Job Description
      </h2>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste the job description here..."
        rows={8}
        className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-y font-body"
      />
    </div>
  );
};

export default JobDescription;
