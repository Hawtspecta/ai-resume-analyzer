import { useState } from "react";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import Header from "@/components/Header";
import ResumeUpload from "@/components/ResumeUpload";
import JobDescription from "@/components/JobDescription";
import ResultsSection from "@/components/ResultsSection";
import { analyzeResume, getMockResult, type AnalysisResult } from "@/lib/api";
import { Button } from "@/components/ui/button";

const Index = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!file) {
      toast.error("Please upload a resume first.");
      return;
    }
    if (!jobDesc.trim()) {
      toast.error("Please paste a job description.");
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const data = await analyzeResume(file, jobDesc);
      setResult(data);
      toast.success("Analysis complete!");
    } catch {
      // Fallback to mock data when backend is unavailable
      toast.info("Backend unavailable — showing demo results.");
      await new Promise((r) => setTimeout(r, 1500));
      setResult(getMockResult());
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8 max-w-3xl space-y-6">
        <div className="grid gap-6 md:grid-cols-2">
          <ResumeUpload file={file} onFileChange={setFile} />
          <JobDescription value={jobDesc} onChange={setJobDesc} />
        </div>

        <div className="flex justify-center">
          <Button
            size="lg"
            onClick={handleAnalyze}
            disabled={loading}
            className="min-w-[200px] font-heading text-base"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing…
              </>
            ) : (
              "Analyze Resume"
            )}
          </Button>
        </div>

        {result && <ResultsSection result={result} />}
      </main>

      <footer className="py-4 text-center text-xs text-muted-foreground">
        AI Resume Analyzer · Built with React & Tailwind
      </footer>
    </div>
  );
};

export default Index;
