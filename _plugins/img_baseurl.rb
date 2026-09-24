Jekyll::Hooks.register [:pages, :posts, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  # Use the effective baseurl (CLI --baseurl overrides _config.yml); a site
  # served from the domain root ("" or "/") needs no rewriting.
  baseurl = doc.site.baseurl.to_s.chomp("/")
  next if baseurl.empty?

  # Prepend baseurl to any src="/..." that doesn't already start with baseurl
  doc.output.gsub!(/ src="(\/(?!#{Regexp.escape(baseurl[1..])}))/,
                   " src=\"#{baseurl}\\1")
end
