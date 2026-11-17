# Publications dated in the future are left out of the site until their date
# has passed, unless they carry `early: true` in the front matter.
#
# That flag is meant for papers that are accepted but not published yet: they
# keep their real publication date (and so appear under the right year) and are
# listed straight away. Without the flag a future-dated entry simply shows up
# on the first build after its date; the deploy workflow runs nightly.
#
# Jekyll's own `future: false` only applies to posts and to documents that are
# written to a page of their own; `publications` is `output: false`, so its
# documents would otherwise all be listed whatever their date. Dropping them
# here, right after reading, covers every listing at once (publications page,
# research-area pages).

Jekyll::Hooks.register :site, :post_read do |site|
  publications = site.collections["publications"]
  next if publications.nil? || site.future

  publications.docs.reject! do |doc|
    doc.date.to_i > site.time.to_i && doc.data["early"] != true
  end
end
