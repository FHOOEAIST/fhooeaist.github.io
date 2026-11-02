# Resolves the `team:` lists of the projects into what the team box of
# _layouts/project.html (_includes/project-team.html) renders.
#
# A project names its team in the front matter, the same list in the DE and
# the EN file, by the ids of member or alumni entries in _data/team.yml:
#
#   team:
#     - christoph-praschl   # first: the contact person
#     - simone-sandler      # the rest: team members, in this order
#
# Sets on every project:
#   team_contact  the first person, if they are still on the team (former
#                 staff can't be contacted), else nil
#   team_members  everyone else, in the order of the list
#
# A person is the team.yml entry merged with "former" (true for alumni
# entries, which get no contact details).
#
# Unknown ids are skipped with a build warning, and so is a DE/EN pair whose
# team lists differ (checked against the EN files on disk, once, in the
# default-language pass).

require "yaml"

module AistProjectTeam
  def self.people(site)
    team = site.data["team"] || {}
    people = {}
    (team["members"] || []).each { |m| people[m["id"]] = m.merge("former" => false) if m["id"] }
    (team["alumni"] || []).each { |m| people[m["id"]] = m.merge("former" => true) if m["id"] }
    people
  end

  # page_id => team list of every EN project file
  def self.en_teams(site)
    Dir[File.join(site.source, "_projects", "en", "*.md")].to_h do |f|
      front = File.read(f, encoding: "UTF-8")[/\A---\s*\n(.*?)\n---/m, 1]
      data = YAML.safe_load(front.to_s, permitted_classes: [Date, Time]) || {}
      [data["page_id"], data["team"]]
    end
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  collection = site.collections["projects"]
  next if collection.nil?

  people = AistProjectTeam.people(site)
  default_pass = !site.respond_to?(:active_lang) || site.active_lang == site.default_lang
  en_teams = default_pass ? AistProjectTeam.en_teams(site) : {}

  collection.docs.each do |doc|
    team = Array(doc.data["team"]).filter_map do |id|
      next people[id] if people[id]
      Jekyll.logger.warn "Project team:", "#{doc.data['page_id']} (#{doc.data['lang']}): unknown member id '#{id}'"
      nil
    end
    contact = team.first unless team.first.nil? || team.first["former"]
    doc.data["team_contact"] = contact
    doc.data["team_members"] = contact ? team.drop(1) : team

    next unless default_pass && doc.data["lang"] == site.config["default_lang"]
    next unless en_teams.key?(doc.data["page_id"]) && en_teams[doc.data["page_id"]] != doc.data["team"]
    Jekyll.logger.warn "Project team:", "#{doc.data['page_id']}: the DE and EN files list different teams"
  end
end
