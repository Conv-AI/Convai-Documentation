# Customer packs

One file per named customer, created with `/new-pack <name> customer` from
`packs/_customer-pack-template.md`.

A customer pack differs from the other two kinds in what it has to settle before anything can be
written: not just how a claim is proven, but **where the resulting pages may be published and who
approves them**. Those pages are not assumed to be public. `docs-writer` refuses to draft against a
customer pack until those fields are filled, which is deliberate - the failure mode here is not a
wrong component name, it is a customer's deployment details on a public site.

This directory is empty until the first customer needs documentation. It exists so that the paths
the skill, the writer, and the planner already point at resolve to something.
