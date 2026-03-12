import { FileText } from "lucide-react";

const Header = () => {
  return (
    <header className="w-full py-8 text-center" style={{ background: "var(--hero-gradient)" }}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="p-2 rounded-xl bg-primary/20 backdrop-blur-sm">
            <FileText className="h-7 w-7 text-primary-foreground" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold font-heading text-primary-foreground tracking-tight">
            AI Resume Analyzer
          </h1>
        </div>
        <p className="text-primary-foreground/70 font-body text-base md:text-lg max-w-md mx-auto">
          Upload your resume, paste a job description, and get instant AI-powered feedback.
        </p>
      </div>
    </header>
  );
};

export default Header;
