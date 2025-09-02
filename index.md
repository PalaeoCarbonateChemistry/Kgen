---
layout: default
title: Home
nav_order: 1
description: "Kgen"
permalink: /
---

# Kgen
{: .fs-9 }

Kgen provides multi-language tools for calculating stoichiometric equilibirium constants (Ks) for seawater at given temperature, salinity, pressure, [Mg] and [Ca].
{: .fs-6 .fw-300 }
[Find out about Kgen](/Kgen/about){: .btn .fs-5 .mb-4 .mb-md-0 }

## Use Kgen

Kgen is available for use in Matlab, Python and R.
{: .fs-6 .fw-300 }
[Kgen in Matlab](/Kgen/use_kgen/matlab){: .btn .fs-5 .mb-4 .mb-md-0 } 
[Kgen in Python](/Kgen/use_kgen/python){: .btn .fs-5 .mb-4 .mb-md-0 }
[Kgen in R](/Kgen/use_kgen/r){: .btn .fs-5 .mb-4 .mb-md-0 }

---

### Cite Kgen

If you use Kgen, please cite:

> Whiteford, R., Branson, O., and Mayk, D. **Using Kgen to Generate Cross-Verified Apparent Equilibrium Constants (K<sup>\*</sup>’s) for Palaeoseawater Carbonate Chemistry.** *G<sup>3</sup>*   [doi:10.1029/2023GC011417](http://doi.org/10.1029/2023GC011417)

### License

Kgen is open-source and distributed under an [MIT license](https://github.com/PalaeoCarb/Kgen/blob/main/LICENSE). You can find the source code on [GitHub](https://github.com/PalaeoCarb/Kgen).

### Contributing

We welcome contributions to Kgen. Please communicate your intentions by first submitting an issue on the [Kgen GitHub repo](https://github.com/PalaeoCarb/Kgen/issues/new), so we can discuss how best to integrate your contributions.

Kgen was built by [Oscar Branson](https://github.com/oscarbranson), [Dennis Mayk](https://github.com/dm807cam), and [Ross Whiteford](https://github.com/rossidae).

#### Thank you all who have contributed to Kgen!

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>
