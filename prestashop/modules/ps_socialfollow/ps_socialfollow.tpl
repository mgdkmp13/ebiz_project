{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * @author    PrestaShop SA <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}

{block name='ps_social_follow'}
  <div class="ps-social-follow">
    <h4>{l s='Follow us' d='Modules.Socialfollow.Shop'}</h4>
    <ul>
      {foreach from=$social_links item='social_link'}
        <li class="{$social_link.class}"><a href="{$social_link.url}">{$social_link.label}</a></li>
      {/foreach}
    </ul>
     <img src="https://localhost:19360/modules/ps_socialfollow/footer-logo.png">

  </div>
{/block}
