<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* @Modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig */
class __TwigTemplate_40d692961a7ce0a2722951cedb9eb83666d0d8161ebc03d96fe85602641c3686 extends \Twig\Template
{
    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->blocks = [
            'content' => [$this, 'block_content'],
            'catalog_categories_listing' => [$this, 'block_catalog_categories_listing'],
            'addon_card_see_more' => [$this, 'block_addon_card_see_more'],
        ];
    }

    protected function doGetParent(array $context)
    {
        // line 19
        return "@PrestaShop/Admin/Module/common.html.twig";
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $this->parent = $this->loadTemplate("@PrestaShop/Admin/Module/common.html.twig", "@Modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig", 19);
        $this->parent->display($context, array_merge($this->blocks, $blocks));
    }

    // line 21
    public function block_content($context, array $blocks = [])
    {
        // line 22
        echo "  <div class=\"row justify-content-center\">
    <div class=\"col-lg-10\">
      ";
        // line 24
        $this->displayBlock('catalog_categories_listing', $context, $blocks);
        // line 43
        echo "    </div>
  </div>
";
    }

    // line 24
    public function block_catalog_categories_listing($context, array $blocks = [])
    {
        // line 25
        echo "        <div class=\"module-short-list\">
          ";
        // line 26
        if (twig_test_empty(($context["modules"] ?? null))) {
            // line 27
            echo "            <div class=\"modules-list module-list-empty\">
              <p>
                ";
            // line 29
            echo twig_escape_filter($this->env, $this->env->getExtension('Symfony\Bridge\Twig\Extension\TranslationExtension')->trans("You do not have any uninstalled module.", [], "Modules.Mbo.Modulescatalog"), "html", null, true);
            echo "
              </p>
            </div>
          ";
        } else {
            // line 33
            echo "            ";
            $this->loadTemplate("@PrestaShop/Admin/Module/Includes/grid_manage_installed.html.twig", "@Modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig", 33)->display(twig_array_merge($context, ["modules" => ($context["modules"] ?? null), "display_type" => "list", "origin" => "manage", "id" => "all"]));
            // line 34
            echo "
            ";
            // line 35
            $this->displayBlock('addon_card_see_more', $context, $blocks);
            // line 40
            echo "          ";
        }
        // line 41
        echo "        </div>
      ";
    }

    // line 35
    public function block_addon_card_see_more($context, array $blocks = [])
    {
        // line 36
        echo "              ";
        if ((twig_length_filter($this->env, ($context["modules"] ?? null)) > ($context["maxModulesDisplayed"] ?? null))) {
            // line 37
            echo "                ";
            $this->loadTemplate("@PrestaShop/Admin/Module/Includes/see_more.html.twig", "@Modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig", 37)->display(twig_array_merge($context, ["id" => "all"]));
            // line 38
            echo "              ";
        }
        // line 39
        echo "            ";
    }

    public function getTemplateName()
    {
        return "@Modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  103 => 39,  100 => 38,  97 => 37,  94 => 36,  91 => 35,  86 => 41,  83 => 40,  81 => 35,  78 => 34,  75 => 33,  68 => 29,  64 => 27,  62 => 26,  59 => 25,  56 => 24,  50 => 43,  48 => 24,  44 => 22,  41 => 21,  31 => 19,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Source("", "@Modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig", "/var/www/html/modules/ps_mbo/views/templates/admin/controllers/module_catalog/uninstalled-modules.html.twig");
    }
}
