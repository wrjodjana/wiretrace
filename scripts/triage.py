import rules

label_rules = [rules.entropy_rule, rules.digit_count_rule, rules.consonant_run_rule, rules.character_set_rule]
domain_rules = [rules.length_rule, rules.label_count_rule]

def score_domain(domain: str) -> dict:
  scores = {}
  for rule in label_rules:
    if rule == rules.entropy_rule:
      scores[rule.__name__] = min(rules.worst_label_score(domain, rule)/4.0, 1.0)
    else:
      scores[rule.__name__] = min(rules.worst_label_score(domain, rule), 1.0)

  scores.update({rule.__name__: min(rule(domain), 1.0) for rule in domain_rules})
  return scores

def triage_packet(packet: dict) -> dict:
  return {**packet, 'scores': score_domain(packet['dns_location'])}

