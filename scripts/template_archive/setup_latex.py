from pathlib import Path


LATEX_DIR = Path("latex")


MAIN_TEX = r"""\documentclass[11pt]{article}

\usepackage[a4paper,margin=1in]{geometry}
\usepackage{setspace}
\usepackage{titlesec}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{tabularx}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\input{harvard-manchester.tex}

\setstretch{1.15}
\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}

\titleformat{\section}{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.5em}{}

\newcommand{\proposalTitle}{Paper Title}
\newcommand{\authorName}{Author Name}
\newcommand{\dateSubmitted}{\today}

\begin{document}

\begin{titlepage}
\centering

\vspace*{3cm}

{\LARGE \bfseries \proposalTitle \par}

\vspace{1.5cm}

\begin{tabular}{rl}
Author: & \authorName \\
Date: & \dateSubmitted
\end{tabular}

\vfill
Institution Name
\end{titlepage}

\tableofcontents
\newpage

\section{Introduction}

Start writing here. Cite an example source with \parencite{example2026}.

\section{Literature Review}

\section{Methods}

\section{Results}

\section{Discussion}

\section{Conclusion}

\printbibliography

\end{document}
"""


HARVARD_MANCHESTER_TEX = r"""% =====================================================
% Harvard (Manchester) citation configuration
% =====================================================

\usepackage[style=british]{csquotes}
\usepackage{xurl}
\def\UrlBreaks{\do\/\do-\do\_\do\.\do\:\do\?\do\&}

\Urlmuskip=0mu plus 1mu

\usepackage[
  backend=biber,
  style=authoryear,
  maxcitenames=2,
  maxbibnames=99,
  uniquelist=false,
  uniquename=init,
  giveninits=true,
  doi=true,
  url=true,
  isbn=false,
  eprint=false,
  date=year
]{biblatex}

\renewcommand*{\bibinitperiod}{.}

\addbibresource{references.bib}

% -----------------------------------------------------
% Harvard punctuation rules
% -----------------------------------------------------

\renewcommand*{\nameyeardelim}{\addcomma\space}
\renewcommand*{\bibpagespunct}{\addcomma\space}
\renewcommand{\multicitedelim}{\addsemicolon\space}
\DeclareFieldFormat{pages}{pp.\space#1}

\DeclareFieldFormat[article]{volume}{#1}
\DeclareFieldFormat[article]{number}{(#1)}

\renewbibmacro{in:}{}

% -----------------------------------------------------
% Formatting tweaks for Harvard
% -----------------------------------------------------

\renewcommand*{\finalnamedelim}{\addspace\&\space}
\setlength{\bibitemsep}{0.6\baselineskip}

\DeclareFieldFormat[article]{title}{\mkbibquote{#1}\addcomma}
\DeclareFieldFormat[book]{title}{#1}

\renewbibmacro*{journal+issuetitle}{%
  \usebibmacro{journal}%
  \setunit{\addcomma\space}%
  \printfield{volume}%
  \printfield{number}%
}

% -----------------------------------------------------
% URL and DOI formatting
% -----------------------------------------------------

\DeclareSourcemap{
  \maps[datatype=bibtex]{
    \map{
      \step[fieldsource=doi,
        match=\regexp{^https?://(dx\.)?doi\.org/},
        replace={}
      ]
    }
  }
}

\DefineBibliographyExtras{british}{%
  \protected\def\mkbibmonth#1{%
    \ifcase#1\or
    January\or February\or March\or April\or May\or June\or
    July\or August\or September\or October\or November\or December%
    \fi}%
}
\DefineBibliographyExtras{english}{%
  \protected\def\mkbibmonth#1{%
    \ifcase#1\or
    January\or February\or March\or April\or May\or June\or
    July\or August\or September\or October\or November\or December%
    \fi}%
}
\ExecuteBibliographyOptions{urldate=long}

\DeclareFieldFormat{urldate}{%
  (Accessed: \thefield{urlday}\space\mkbibmonth{\thefield{urlmonth}}\space\thefield{urlyear})%
}

\DeclareFieldFormat{doi}{\url{https://doi.org/#1}}
\DeclareFieldFormat{url}{\url{#1}}

\renewbibmacro*{doi+eprint+url}{%
  \iffieldundef{doi}
    {%
      \iffieldundef{url}
        {}
        {%
          \setunit{\adddot\space}%
          \printtext{Available at:\space}%
          \printfield{url}%
          \setunit{\addspace}%
          \printurldate
        }%
    }
    {%
      \setunit{\adddot\space}%
      \printfield{doi}%
    }%
}

% -----------------------------------------------------
% Tech report formatting
% -----------------------------------------------------

\DeclareBibliographyDriver{report}{%
  \printnames{author}%
  \setunit{\addspace}%
  \printtext[parens]{\printfield{year}}\adddot\space
  \printfield{title}\adddot\space
  \printlist{institution}\addcomma\space
  \printfield{number}\adddot\space
  \usebibmacro{doi+eprint+url}%
  \finentry
}
"""


REFERENCES_BIB = r"""@online{example2026,
  author = {{Example Author}},
  title = {Example Reference},
  year = {2026},
  url = {https://example.com},
  urldate = {2026-04-24}
}
"""


def write_file(path: Path, content: str, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        print(f"Skipped existing file: {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote: {path}")


def main() -> None:
    LATEX_DIR.mkdir(parents=True, exist_ok=True)

    for subdir in ["sections", "figures", "tables"]:
        (LATEX_DIR / subdir).mkdir(parents=True, exist_ok=True)

    write_file(LATEX_DIR / "main.tex", MAIN_TEX)
    write_file(LATEX_DIR / "harvard-manchester.tex", HARVARD_MANCHESTER_TEX)
    write_file(LATEX_DIR / "references.bib", REFERENCES_BIB)

    print("\nLaTeX template generated.")
    print("Compile with:")
    print("  make latex")
    print("\nOr manually:")
    print("  cd latex")
    print("  latexmk -pdf main.tex")


if __name__ == "__main__":
    main()