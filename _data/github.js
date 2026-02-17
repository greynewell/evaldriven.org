const { execSync } = require("child_process");

module.exports = function () {
  const repo = "greynewell/evaldriven.org";

  // Fetch all stargazers (paginated)
  const stargazers = [];
  let page = 1;
  while (true) {
    try {
      const result = execSync(
        `gh api "repos/${repo}/stargazers?per_page=100&page=${page}" --jq ".[].login"`,
        { timeout: 30000, encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] }
      ).trim();
      if (!result) break;
      stargazers.push(...result.split("\n").filter(Boolean));
      page++;
    } catch {
      break;
    }
  }

  // Fetch repo stats
  let forks = 0;
  let watchers = 0;
  try {
    const result = execSync(
      `gh api "repos/${repo}" --jq "[.forks_count, .subscribers_count] | @tsv"`,
      { timeout: 30000, encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] }
    ).trim();
    const parts = result.split("\t");
    forks = parseInt(parts[0], 10) || 0;
    watchers = parseInt(parts[1], 10) || 0;
  } catch {
    // ignore
  }

  return { stargazers, forks, watchers };
};
