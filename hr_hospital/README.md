# Hospital Management: model views and automation

This module manages doctors, patients, diseases, and patient visits. The
following changes expand the model presentation and automate routine visit
maintenance.

## Patient visits

- The form now has a clickable three-state status bar, all visit fields,
  chatter, and a stat button. The stat button counts and opens only visits
  with the same disease.
- List, search, calendar, pivot, and stacked bar chart views are available.
  The visit action opens with a current-year filter; pivot rows are doctors
  and months, its columns are statuses, and the graph groups months by
  disease.
- The search panel filters by doctor and hierarchical disease. Because the
  disease model uses `parent_id` and `_parent_store`, parent disease selection
  includes visits assigned to descendant diseases.
- `mail.thread` tracks changes to the visit status and doctor only, so the
  chatter shows meaningful history without recording unrelated edits.

## Patients and doctors

- Patient search supports both name and phone. The patient form shows the
  complete medical data, a visit-history stat button, and a header action to
  create a visit with patient, personal doctor, and disease prefilled.
- Doctor search includes distinct mentor and intern filters. Doctors have a
  qualification-grouped kanban view, an archive-aware card menu, and a card
  action to create a visit prefilled with that doctor. Mentor forms show their
  interns in an embedded kanban.
- Quick visit creation uses model `type="object"` actions. This centralizes
  context defaults in Python for the patient and doctor entry points. A
  separate XML action with context defaults was considered, but rejected
  because it would duplicate that context in two places.

## Disease report wizard

The **Print** menu on doctor list and form views contains *Patient Visit
Report*. Its optional doctors, diseases, and inclusive date range build a
visit list immediately grouped by disease. An empty wizard intentionally uses
an empty domain and therefore returns all visits. The ending date is converted
to the next midnight with a strict `<` comparison, which includes every visit
on the selected final day.

## Automatic overdue-visit cancellation

`Cancel Overdue Patient Visits` is an `ir.actions.server` action available in
the visit list action menu and an `ir.cron` job scheduled daily. Both invoke
the short model method `_cron_cancel_overdue_visits()`, which independently
searches planned visits whose scheduled datetime has passed and changes their
state to cancelled. The cron is module data, so it is removed with the module.

## Demo data

Demo data now includes two additional intern doctors under a mentor and six
additional visits distributed across February through August 2026. These give
the calendar, pivot, and stacked chart data in several months and diseases.
