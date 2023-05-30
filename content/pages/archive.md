Title: Archive
Status: published

<div class="container-fluid">
  <div class="row">
    <div class="col-md">
      {% filter markdown %}
        {% include "pages/archive-recent.md" %}
      {% endfilter %}
    </div>
    <div class="col-md">
      {% filter markdown %}
        {% include "pages/archive-university.md" %}
      {% endfilter %}
    </div>
  </div>
</div>
