/**
 *
 * Bootstrap Callout Helper
 *
 * Syntax:
 *   {% callout [type] %}
 *   Callout content
 *   {% endcallout %}
 *
 *
 * Type Colors:
 *   default: grey
 *   primary: blue
 *   success: green
 *   info: light blue
 *   warning: orange
 *   danger: red
 *
 * Type colors are used for the panel's left border, <h4> tags, and Font Awesome icons.
 *   
**/

hexo.extend.tag.register('callout', function(args, content) {
  var calloutType = args.length ? args[0] : 'default';
  var result = '';
  result += '<div class="bs-callout bs-callout-' + calloutType + '">';
  result += hexo.render.renderSync({text: content, engine: 'markdown'});
  result += '</div>';
  return result;
}, true);