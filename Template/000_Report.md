---
title: REPORT_TITLE
author: Lukas Harlan
date: 2025-04-29
toc: true
version: "1.0"
toc-depth: "2"
---

# Introduction
TEXT

# Management Summary
## Overview Findings


| Id  | Name | Severity |
| --- | ---- | -------- |
{% for f in findings -%}
| {{ f.id }} | {{ f.title }} | {{ f.Severity }} | 
{% endfor %}

## Summary
## Conclusion

# Scope

| IP / URL | Name | Details |
| -------- | ---- | ------- |
|          |      |         |
|          |      |         |

# Findings
```{.include}
{% for f in findings -%}
Findings/{{ f.filename }}
{% endfor %}
```
# Appendix
TEST
