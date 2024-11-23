<?php
/* Smarty version 3.1.48, created on 2024-11-16 19:11:37
  from '/var/www/html/admin123/themes/default/template/controllers/tax_rules/helpers/list/list_action_edit.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_6738e0598cede8_21827118',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '98cfddf7702bd492324d6d7b67179c1e0c6e9eb7' => 
    array (
      0 => '/var/www/html/admin123/themes/default/template/controllers/tax_rules/helpers/list/list_action_edit.tpl',
      1 => 1702485415,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_6738e0598cede8_21827118 (Smarty_Internal_Template $_smarty_tpl) {
?><a onclick="loadTaxRule('<?php echo call_user_func_array($_smarty_tpl->registered_plugins[ 'modifier' ][ 'escape' ][ 0 ], array( $_smarty_tpl->tpl_vars['id']->value,'html','UTF-8' ));?>
'); return false;" href="#" class="btn btn-default">
	<i class="icon-pencil"></i>
	<?php echo $_smarty_tpl->tpl_vars['action']->value;?>

</a>
<?php }
}
