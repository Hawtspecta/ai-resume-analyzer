import { motion } from "framer-motion";
import { CheckCircle2, XCircle, Lightbulb, GraduationCap } from "lucide-react";
import type { AnalysisResult } from "@/lib/api";

interface ResultsSectionProps {
  result: AnalysisResult;
}

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0 },
};

const ResultsSection = ({ result }: ResultsSectionProps) => {
  const matchColor =
    result.skill_match >= 80
      ? "text-green-600"
      : result.skill_match >= 50
      ? "text-yellow-600"
      : "text-destructive";

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid gap-5 md:grid-cols-2"
    >
      {/* Skill Match */}
      <motion.div
        variants={item}
        className="rounded-xl border border-border bg-card p-6 card-elevated flex flex-col items-center justify-center"
      >
        <CheckCircle2 className="h-8 w-8 text-primary mb-2" />
        <h3 className="text-sm font-medium text-muted-foreground font-heading uppercase tracking-wide mb-1">
          Skill Match
        </h3>
        <p className={`text-5xl font-bold font-heading ${matchColor}`}>
          {result.skill_match}%
        </p>
      </motion.div>

      {/* Missing Skills */}
      <motion.div
        variants={item}
        className="rounded-xl border border-border bg-card p-6 card-elevated"
      >
        <div className="flex items-center gap-2 mb-3">
          <XCircle className="h-5 w-5 text-destructive" />
          <h3 className="text-sm font-medium text-muted-foreground font-heading uppercase tracking-wide">
            Missing Skills
          </h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {result.missing_skills.map((skill) => (
            <span
              key={skill}
              className="inline-block rounded-full bg-destructive/10 px-3 py-1 text-xs font-medium text-destructive"
            >
              {skill}
            </span>
          ))}
        </div>
      </motion.div>

      {/* Suggestions */}
      <motion.div
        variants={item}
        className="rounded-xl border border-border bg-card p-6 card-elevated"
      >
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb className="h-5 w-5 text-primary" />
          <h3 className="text-sm font-medium text-muted-foreground font-heading uppercase tracking-wide">
            Suggestions
          </h3>
        </div>
        <ul className="space-y-2">
          {result.suggestions.map((s, i) => (
            <li key={i} className="text-sm text-card-foreground flex gap-2">
              <span className="text-primary font-bold">›</span> {s}
            </li>
          ))}
        </ul>
      </motion.div>

      {/* Learning Path */}
      <motion.div
        variants={item}
        className="rounded-xl border border-border bg-card p-6 card-elevated"
      >
        <div className="flex items-center gap-2 mb-3">
          <GraduationCap className="h-5 w-5 text-primary" />
          <h3 className="text-sm font-medium text-muted-foreground font-heading uppercase tracking-wide">
            Learning Path
          </h3>
        </div>
        <ol className="space-y-2">
          {result.learning_path.map((step, i) => (
            <li key={i} className="text-sm text-card-foreground flex gap-2">
              <span className="text-primary font-bold font-heading">{i + 1}.</span> {step}
            </li>
          ))}
        </ol>
      </motion.div>
    </motion.div>
  );
};

export default ResultsSection;
