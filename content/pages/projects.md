Title: Projects
Status: published

{% for project in projects %}
<div class="card mb-3">
<div class="card-body">
 <h5 class="card-title">{{project.name}}</h5>
{{project.desc|markdown}}
{% for link in project.links %}
<a href="{{link.href}}" class="card-link">{{link.name}}</a>
{% endfor %}
</div>
</div>
{% endfor %}
