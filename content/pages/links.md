Title: Links
Status: published

A collection of links to other places on the internet I find interesting.

<div class="row">
    {% for col in [links.left, links.right] %}
    <div class="col-md">
      {% for section in col %}
      <h3>{{section.heading}}</h3>
      <ul>
        {% for link in section.links %}
        <li><a href="{{link.href}}">{{link.name}}</a></li>
        {% endfor %}
      </ul>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
