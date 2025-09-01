<figure style="margin-inline: block;">
  <img src="https://bedrock.engineer/public/Bedrock_TextRight.png" alt="Bedrock logo" width="75%"/>
</figure>

<h3 style="margin-inline: block;">Bedrock, the Open-Source Foundation for Geotechnical Engineering</h3>

---

[![Tests](https://github.com/bedrock-engineer/bedrock-ge/actions/workflows/tests.yml/badge.svg?event=push&branch=main)](https://github.com/bedrock-engineer/bedrock-ge/actions/workflows/tests.yml?query=event%3Apush+branch%3Amain)
[![PyPI](https://img.shields.io/pypi/v/bedrock-ge)](https://pypi.org/project/bedrock-ge/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16270261.svg)](https://doi.org/10.5281/zenodo.16270261)

---

🌐 **Website:** <https://bedrock.engineer>

📖 **Documentation:** <https://bedrock.engineer/docs>

📑 **API Reference:** <https://bedrock.engineer/reference>

🖥️ **Source Code:** <https://github.com/bedrock-engineer/bedrock-ge>

🐍 **`bedrock-ge` on PyPI:** <https://pypi.org/project/bedrock-ge>

🔗 **LinkedIn:** <https://www.linkedin.com/company/bedrock-engineer>

---

## Overview

> **Definition of Bedrock**
>
> In an abstract sense, the bedrock refers to the main principles something is based on. [1]
>
> In the real world, the bedrock is the hard area of rock in the ground that holds up the loose soil above. [1]
>
> In many civil engineering projects, the identification of the bedrock through digging, drilling or geophysical methods is an important task, which greatly influences (geotechnical) design. [2]
>
> Sources: [[1] Bedrock | Cambridge Dictionary](https://dictionary.cambridge.org/us/dictionary/english/bedrock), [[2] Bedrock | Wikipedia](https://en.wikipedia.org/wiki/Bedrock)

Ground Investigation (GI) data is often trapped in legacy formats that limit analysis and visualization possibilities.
`bedrock-ge` lets you transform this data from specialized geotechnical formats and common tabular formats (Excel, CSV) into modern, standardized geospatial data.

This standardization lets you bridge the gap between raw geotechnical data, the modern Python (geo)scientific ecosystem and modern geospatial tools.
This gives geotechnical engineers greater flexibility in visualization, modeling, and integration across different software environments while avoiding vendor lock-in.
For example, this enables connecting your GI data with GIS as well as BIM environments through [platforms like Speckle](#-put-your-gi-data-into-speckle).

The purpose of Bedrock is NOT to become THE standard for geotechnical data, because [we don't need 15 instead of 14 competing standards](https://xkcd.com/927/). 

## Highlights

### 📖 Read / write Ground Investigation (GI) data in different formats

| Data Format | Read | Write |
| ----------- | ---- | ----- |
| AGS 3       | ✅   | ❌    |
| AGS 4       | ✅   | ✅    |
| Excel       | ✅   | ✅    |
| CSV         | ✅   | ✅    |
| JSON        | ✅   | ✅    |
| GeoJSON     | ✅   | ✅    |

Do you need another format? Like [DIGGS](https://diggsml.org/), [NADAG](https://www.ngu.no/geologisk-kartlegging/om-nadag-nasjonal-database-grunnundersokelser), [GEF](https://publicwiki.deltares.nl/display/STREAM/Dutch+National+GEF+Standards), or something else?
Let us know by creating an [issue](https://github.com/bedrock-engineer/bedrock-ge/issues) or starting a [discussion](https://github.com/orgs/bedrock-engineer/discussions).

Also, if you have a project with publicly available GI data, please share that in a [discussion](https://github.com/orgs/bedrock-engineer/discussions), such that we can create a tutorial from it.

### ✅ Validate your GI data

`bedrock-ge` comes with data validation to make sure that you can combine Ground Investigation data from multiple files into a single geospatial database with consistent relationships between GI locations, samples, in-situ measurements and lab tests.

This data validation mechanism (based on [`pandera`](https://pandera.readthedocs.io/en/stable/)) is easily extensible, giving you the power to add your own data validation criteria.

### 🗺️ Put your GI data from multiple files into a single 3D geospatial database

For example, you can take GI data from 100 AGS files and combine them into a single a [GeoPackage](https://en.wikipedia.org/wiki/GeoPackage) ([like a Shapefile, but then waaay better](http://switchfromshapefile.org/)). Such a GeoPackage can then be loaded into ArcGIS, where you can visualize your GI data in 3D:

<figure style="margin-inline: block; display: block;">
  <img src="https://bedrock.engineer/public/images/KaiTak_BrGI_ArcGIS.webp" alt="Kai Tak, Hong Kong, 3D GI data visualization in ArcGIS" width="90%"/> 
  <figcaption>
  GI data in Kai Tak, Hong Kong. <a href="https://arcg.is/0r9DG9">Click here to explore for yourself.</a>
</figcaption>
</figure>

### 🟦 Put your GI data into Speckle

From ArcGIS or QGIS you can publish your GI data to [Speckle](https://speckle.systems/) and then visualize it together with your ground models and civil engineering designs:

<figure style="margin-inline: block; display: block;">
  <img src="https://bedrock.engineer/public/images/KaiTak_BrGI_Speckle.png" alt="Kai Tak, Hong Kong, data from many sources in Speckle." width="90%"/> 
  <figcaption>
  Models from Rhino, Revit, Civil3D + context & GI data from Q/ArcGIS. <a href="https://app.speckle.systems/projects/013aaf06e7/models/0fa0287ba8,1cbe68ed69,44c8d1ecae,7f9d99cae2,9535541c2b,a739490298,ff81bfa02b">Click here to explore for yourself.</a>
</figcaption>
</figure>

<figure style="margin-inline: block; display: block;">
  <img src="https://bedrock.engineer/public/images/WekaHills_Speckle.webp" alt="GI data, the derived Leapfrog ground model and a tunnel in Speckle." width="90%"/> 
  <figcaption>
  GI data, the derived Leapfrog ground model and a tunnel in Speckle. <a href="https://app.speckle.systems/projects/7a489ac0d4/models/$epsg:2193-7839%2Fgeo%2Fgeology-model,65b4cf97d5,9069ef2b2b">Click here to explore for yourself.</a>
</figcaption>
</figure>

Moreover, your GI data becomes available in all the software that [Speckle has connectors for](https://app.speckle.systems/downloads).

### 🔓 Free and Open Source Software

`bedrock-ge` is Free and Open Source Software (FOSS), meaning it gives you full access to the code, and you can customize `bedrock-ge` to integrate with other tools and fit your workflows and project needs.

As the name implies, FOSS is free to use, so you're not tied to expensive software licenses or locked into a specific software vendor.

You can give [feedback](#-feedback) and [contribute](#-contributing), such that together we can build the tools we've always wanted and needed.

## Installation

We recommend to use [`uv`](https://docs.astral.sh/uv/) to manage Python for you.
Using `uv`, you can add `bedrock-ge` to your Python project and install it in your project's virtual environment by running:

```bash
uv add bedrock-ge
```

It's also possible to install `bedrock-ge` from [PyPI](https://pypi.org/project/bedrock-ge/) (Python Packaging Index) using `pip`:

```bash
pip install bedrock-ge
```

## Feedback

Got some feedback, a great idea, running into problems when working with Bedrock or just want to ask some questions?

Please feel free to:

1. Open an issue for feature requests or bug reports: [`bedrock-ge` issues](https://github.com/bedrock-engineer/bedrock-ge/issues),
2. Start a discussion in this GitHub repo: [Bedrock discussions](https://github.com/orgs/bedrock-engineer/discussions),
3. Or start a discussion on the Speckle community forum if that's more appropriate: [Speckle community forum](https://speckle.community/)

All feedback and engagement with the Bedrock community is welcome.

## Contributing

Contributing isn't scary. Contributing isn't just about writing code:

- Spread the word about Bedrock
- Use Bedrock and provide [feedback](#-feedback)
- Share how you use Bedrock
- Help each other out, e.g. by replying to questions in the [discussions](https://github.com/orgs/bedrock-engineer/discussions) or [`bedrock-ge` issues](https://github.com/bedrock-engineer/bedrock-ge/issues)
- Documentation and tutorials
- Most pages on the [bedrock.engineer](https://bedrock.engineer/) website can be edited, so if you see a spelling mistake or have a suggestion on how to explain something better, click this button to make a contribition.

<figure style="margin-inline: block;">
  <img src="https://bedrock.engineer/public/images/EditThisPage.png" alt="Edit this page on GitHub button on bedrock.engineer" width="25%"/>
</figure>

- If you would like to contribute code, awesome!
  Please create an [issue](https://github.com/bedrock-engineer/bedrock-ge/issues) for what you'd like to contribute. If you don't know how to get started, please indicate this in your issue, and we'll help you out.

## Maintainers

### Joost

> I studied geotechnical engineering and applied geophysics and then worked for [Arup](https://www.arup.com/) for 4 years as a geotechnical engineer and [computational designer](https://www.arup.com/services/computational-and-parametric-design/).
>
> During my time at Arup I worked a lot on bringing computational design into the world of geotechnical engineering, and on [bridging the gaps between geotechnical engineering and structural engineering](https://www.linkedin.com/posts/joost-gevaert_lightbim-lightbim-lightbim-activity-7234726439835549697-3xdO).
>
> Bedrock is the Free and Open Source Software (FOSS) that I wish existed when I worked as a geotechnical engineer at Arup.

### Jules

> I studied Applied Geoscience (Petroleum Engineering Reservoir Geology) but frustration with technical software led me to learn to code and as a result, I mostly worked in software development.
>
> Over the past 5 years, I’ve worked on data-rich applications across various domains, specifically in frontend development.
> My primary interest is figuring out how to build tools for more thoughtful display and processing of technical information, for geoscience in particular.

## Contributors

Please take a look at the [contributors page](https://github.com/bedrock-engineer/bedrock-ge/graphs/contributors).

## Professional Support

While `bedrock-ge` is an Free Open Source Software (FOSS) project, you might be looking for professional support implementing it, contact <info@bedrock.engineer> for more information.
