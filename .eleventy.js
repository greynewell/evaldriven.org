const markdownIt = require("markdown-it");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("og.png");

  const md = markdownIt({ html: true, linkify: true });
  eleventyConfig.addFilter("markdown", (content) => {
    return content ? md.render(content) : "";
  });

  eleventyConfig.addFilter("date", (value, format) => {
    const d = value ? new Date(value) : new Date();
    if (format === "iso") return d.toISOString();
    return d.toISOString().split("T")[0];
  });

  eleventyConfig.addFilter("json", (value) => JSON.stringify(value));

  return {
    dir: {
      input: ".",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
  };
};
