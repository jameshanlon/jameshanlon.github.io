Title: Archive
Status: published

<div class="container-fluid">
  <div class="row">
    <div class="col-sm">
      {% filter markdown %}
        {% include "pages/archive-recent.md" %}
      {% endfilter %}
    </div>
    <div class="col-sm article-list">
      {% filter markdown %}
        {% include "pages/archive-university.md" %}
      {% endfilter %}
    </div>
  </div>
</div>
