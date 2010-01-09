<?php
// $Id: template.php,v 1.4.2.1 2007/04/18 03:38:59 drumm Exp $

/**
 * Sets the body-tag class attribute.
 *
 * Adds 'sidebar-left', 'sidebar-right' or 'sidebars' classes as needed.
 */
function phptemplate_body_class($sidebar_left, $sidebar_right) {
  if ($sidebar_left != '' && $sidebar_right != '') {
    $class = 'sidebars';
  }
  else {
    if ($sidebar_left != '') {
      $class = 'sidebar-left';
    }
    if ($sidebar_right != '') {
      $class = 'sidebar-right';
    }
  }

  if (isset($class)) {
    print ' class="'. $class .'"';
  }
}

/**
 * Return a themed breadcrumb trail.
 *
 * @param $breadcrumb
 *   An array containing the breadcrumb links.
 * @return a string containing the breadcrumb output.
 */
/* Commented out to provide a breadcrumb with title of current page -- below
function phptemplate_breadcrumb($breadcrumb) {
  if (!empty($breadcrumb)) {
    return '<div class="breadcrumb">'. implode(' › ', $breadcrumb) .'</div>';
  }
}
*/

/*
    phptemplate_breadcrumb($breadcrumb) modification
    File: template.php
    Use: Hide breadcrumb trails with only 1 crumb, regardless of crumb name ("home" is)
        a popular single-crumb that people like to have removed in some templates.
    Through: PHPTemplate function override
    Benefits: Does not involve extra code in separate view.
*/
function phptemplate_breadcrumb($breadcrumb) {
    $home = variable_get('site_name', 'drupal');
    $sep = ' &raquo; ';
    // Check if breadcrumb has more than 1 element.
    // Options: Change to the number of elements/crumbs a breadcrumb needs to be visible.
    if (count($breadcrumb) > 0) {
        $breadcrumb[0] = l(t($home), '');
        /*
            Optional: Include page title in breadcrumb.
       
            drupal_get_title() !== ''
                Check if title blank, if that is the case, we cannot include trailing page name.
            strstr(end($breadcrumb),drupal_get_title()) == FALSE
                Some modules will make it so path or breadcrumb will involve duplication of
                title and node name (such as in the Events module) to remove this, simply
                take out  && strstr(end($breadcrumb),drupal_get_title()) == FALSE
           
            Use: Simply uncomment the if structure below (3 lines).
            Special Use: If you wish to use this regardless of elements/crumbs in a breadcrumb
                simply cut/paste the statements inside the "if (count($breadcrumb) > 1)" outside
                of the structure, and delete the extranneous structure.
        */       
            if ( (drupal_get_title() !== '') && (strstr(end($breadcrumb),drupal_get_title()) ) == FALSE) {
                $breadcrumb[] = t(drupal_get_title(), '');
            }
       
        return '<div class="breadcrumb">'. implode($sep, $breadcrumb) .'</div>';
    } else {
        // Would only show a single element/crumb (or none), so return nothing.
        // You can remove this statement.
    }
}

/**
 * Allow themable wrapping of all comments.
 */
function phptemplate_comment_wrapper($content, $type = null) {
  static $node_type;
  if (isset($type)) $node_type = $type;

  if (!$content || $node_type == 'forum') {
    return '<div id="comments">'. $content . '</div>';
  }
  else {
    return '<div id="comments"><h2 class="comments">'. t('Comments') .'</h2>'. $content .'</div>';
  }
}

/**
 * Override or insert PHPTemplate variables into the templates.
 */
function _phptemplate_variables($hook, $vars) {
  if ($hook == 'page') {

    if ($secondary = menu_secondary_local_tasks()) {
      $output = '<span class="clear"></span>';
      $output .= "<ul class=\"tabs secondary\">\n". $secondary ."</ul>\n";
      $vars['tabs2'] = $output;
    }

    // Hook into color.module
    if (module_exists('color')) {
      _color_page_alter($vars);
    }
    return $vars;
  }
  return array();
}

/**
 * Returns the rendered local tasks. The default implementation renders
 * them as tabs.
 *
 * @ingroup themeable
 */
function phptemplate_menu_local_tasks() {
  $output = '';

  if ($primary = menu_primary_local_tasks()) {
    $output .= "<ul class=\"tabs primary\">\n". $primary ."</ul>\n";
  }

  return $output;
}


/**
 * Declare the available regions implemented by this engine.
 *
 * @return
 *  An array of regions. The first array element will be used as the default region for themes.
 */
function StartPad_v2_regions() {
  return array(
       'left' => t('left sidebar'),
       'right' => t('right sidebar'),
       'content_top' => t('content top'),
       'content' => t('content'),
       'header' => t('header'),
       'header_right' => t('header right'),
       'footer' => t('footer')
  );
}
  
/* A function to display the next countdown even on the front page in a themed box */
function StartPad_v2_views_view_list_countdownNext($view, $nodes) {
	$node = $nodes[0];

/*
print '<pre>';
print_r($node);
print '</pre>';
*/

	$sUrl = url("node/".$node->nid);
	$sATag = "<a href=\"" . $sUrl . "\">";
	$st = "";
	$st .= "<div class=\"CountdownTitle\">";
	$st .= $sATag . "<h1>StartPad Countdown #" . $node->node_data_field_countdownnumber_field_countdownnumber_value . "</h1></a>";
	$st .= "</div>";
	$st .= "<div class=\"CountdownBody\">";
	$st .= $sATag . "<h2>" . $node->node_title . "</h2></a>";
	$st .= "<p><i>" . $node->node_data_field_countdownspeaker_field_countdownspeaker_value . "</i></p>";
	$st .= "<h2>" . $node->node_data_field_countdownwhen_field_countdownwhen_value . "</h2>";
	$st .= "<input class=\"Signup\" type=\"button\" value=\"Sign Up\" onclick=\"location.href='" . $sUrl . "';\"/>";
	$st .= "</div>";



	return $st;
}
