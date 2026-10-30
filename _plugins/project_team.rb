# Resolves the `team:` lists of the projects into what the team box of
# _layouts/project.html (_includes/project-team.html) renders.
#
# A project names its team in the front matter, the same block in the DE and
# the EN file:
#
#   team:
#     - member: christoph-praschl   # id of a member or alumni entry in _data/team.yml
#       role: lead                  # id from _data/project_roles.yml
#       contact: true               # optional, shown first as the contact person
#       years: 2021–2023            # optional, if the person was only on it for a while
#
# A phase in the `projects:` list can carry its own `team:` when the team
# changed between phases; phases without one use the project-level list.
#
# Sets on every project:
#   team_groups   one group per distinct team, latest phase first:
#                 { "phases" => [2, 3], "members" => [person, ...] }, members
#                 sorted by role, then last name. A single group (the usual
#                 case) has no "phases", so the box shows no phase headings.
#   team_contact  the contact person of the latest group (`contact: true`, else
#                 its first current lead), or nil; left out of the list when
#                 there is only one group
#
# A person is the team.yml entry merged with "role", "years", "contact" and
# "former" (true for alumni entries, which get no contact details).
#
# Unknown member or role ids are skipped with a build warning, and so is a
# DE/EN pair whose team lists differ (checked against the twin file on disk,
# once, in the default-language pass).

require "yaml"

module AistProjectTeam
  DEGREE = /\A(?:MSc|BSc|MA|BA|MBA|PhD|DI|MEng|BEng|Mag|Dr|Prof)\z/

  def self.last_name_key(name)
    words = name.to_s.split(/\s+/).reject { |w| w.include?(".") || w.include?("(") || w =~ DEGREE }
    key = (words.last || name).to_s.downcase
    key.gsub("ä", "ae").gsub("ö", "oe").gsub("ü", "ue").gsub("ß", "ss")
  end

  def self.people(site)
    team = site.data["team"] || {}
    people = {}
    (team["members"] || []).each { |m| people[m["id"]] = m.merge("former" => false) if m["id"] }
    (team["alumni"] || []).each { |m| people[m["id"]] = m.merge("former" => true) if m["id"] }
    people
  end

  def self.resolve(list, people, roles, where)
    Array(list).filter_map do |entry|
      person = people[entry["member"]]
      unless person
        Jekyll.logger.warn "Project team:", "#{where}: unknown member id '#{entry['member']}'"
        next
      end
      unless roles.key?(entry["role"])
        Jekyll.logger.warn "Project team:", "#{where}: unknown role '#{entry['role']}' for #{entry['member']}"
      end
      person.merge(
        "role" => entry["role"],
        "years" => entry["years"] || (person["former"] ? person["years"] : nil),
        "contact" => entry["contact"] == true && !person["former"]
      )
    end.sort_by { |p| [roles.fetch(p["role"], roles.size), last_name_key(p["name"])] }
  end

  # the `team:` blocks of a front matter, for comparing the DE and EN file
  def self.team_blocks(data)
    [data["team"]] + Array(data["projects"]).map { |p| p.is_a?(Hash) ? p["team"] : nil }
  end

  def self.check_twin(doc)
    return unless doc.path.include?("/_projects/de/") || doc.path.include?("\\_projects\\de\\")
    twin = doc.path.sub(%r{([/\\])_projects([/\\])de([/\\])}, '\1_projects\2en\3')
    return unless File.exist?(twin)
    front = File.read(twin, encoding: "UTF-8")[/\A---\s*\n(.*?)\n---/m, 1]
    data = YAML.safe_load(front.to_s, permitted_classes: [Date, Time]) || {}
    return if team_blocks(doc.data) == team_blocks(data)
    Jekyll.logger.warn "Project team:", "#{doc.data['page_id']}: the DE and EN files list different teams"
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  collection = site.collections["projects"]
  next if collection.nil?

  people = AistProjectTeam.people(site)
  roles = Array(site.data["project_roles"]).each_with_index.to_h { |r, i| [r["id"], i] }
  default_pass = !site.respond_to?(:active_lang) || site.active_lang == site.default_lang

  collection.docs.each do |doc|
    where = "#{doc.data['page_id']} (#{doc.data['lang']})"
    phases = Array(doc.data["projects"])
    lists = phases.empty? ? [doc.data["team"]] : phases.map { |p| p["team"] || doc.data["team"] }

    groups = []
    lists.each_with_index do |list, i|
      next if Array(list).empty?
      group = groups.find { |g| g["list"] == list }
      if group
        group["phases"] << i + 1
      else
        groups << { "list" => list, "phases" => [i + 1] }
      end
    end

    groups = groups.reverse.map do |g|
      members = AistProjectTeam.resolve(g["list"], people, roles, where)
      { "phases" => g["phases"], "members" => members }
    end
    groups.each { |g| g.delete("phases") } if groups.size == 1

    contact = nil
    if (latest = groups.first)
      contact = latest["members"].find { |p| p["contact"] } ||
                latest["members"].find { |p| p["role"] == "lead" && !p["former"] }
      # with phase groups the contact stays in its phase, so each phase lists its whole team
      latest["members"] = latest["members"].reject { |p| p.equal?(contact) } if contact && groups.size == 1
    end

    doc.data["team_groups"] = groups
    doc.data["team_contact"] = contact

    AistProjectTeam.check_twin(doc) if default_pass
  end
end
