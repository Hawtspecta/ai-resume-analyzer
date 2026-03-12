import { useState } from "react";
import axios from "axios";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import Header from "@/components/Header";
import ResumeUpload from "@/components/ResumeUpload";
import JobDescription from "@/components/JobDescription";
import ResultsSection from "@/components/ResultsSection";
import { analyzeResume, getMockResult, uploadResume, type AnalysisResult } from "@/lib/api";
import { Button } from "@/components/ui/button";

const Index = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
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
    setError(null);
    setResult(null);

    try {
      const { extracted_text } = await uploadResume(file);
      const data = await analyzeResume(extracted_text, jobDesc);
      setResult(data);
      toast.success("Analysis complete!");
    } catch (err: unknown) {
      const message =
        axios.isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : err instanceof Error
          ? err.message
          : "An unexpected error occurred.";

      setError(message);
      toast.error(message);

      // Fallback to mock data when backend is unavailable (optional)
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

        <div className="flex flex-col items-center gap-3">
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

          {error && (
            <p className="text-sm text-destructive text-center max-w-xl">
              {error}
            </p>
          )}
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
