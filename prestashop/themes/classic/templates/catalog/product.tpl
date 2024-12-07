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
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA
 * @copyright Since 2007 PrestaShop SA
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}

{extends file=$layout}

{block name='head' append}
  <meta property="og:type" content="product">
  {if $product.cover}
    <meta property="og:image" content="{$product.cover.large.url}">
  {/if}

  {if $product.show_price}
    <meta property="product:pretax_price:amount" content="{$product.price_tax_exc}">
    <meta property="product:pretax_price:currency" content="{$currency.iso_code}">
    <meta property="product:price:amount" content="{$product.price_amount}">
    <meta property="product:price:currency" content="{$currency.iso_code}">
  {/if}

  {if isset($product.weight) && $product.weight != 0}
    <meta property="product:weight:value" content="{$product.weight}">
    <meta property="product:weight:units" content="{$product.weight_unit}">
  {/if}
{/block}

{block name='head_microdata_special'}
  {include file='_partials/microdata/product-jsonld.tpl'}
{/block}

{block name='content'}
  <div class="info">
    <a href=".">
      <h2>INFORMACJE O DOSTAWIE!</h2>
    </a>
  </div>
  <div class="info2">
    <a href=".">
      <h2>NOWE ZESTAWY PREZENTOWE JUŻ DOSTĘPNE!</h2>
    </a>
  </div>
<section id="main">
  <meta content="{$product.url}">
  <div class="row product-container js-product-container">

    <!-- Product Images and Thumbnails -->
    <div class="col-md-6">
      {block name='product_images'}
        <section class="page-content" id="content">
          {include file='catalog/_partials/product-flags.tpl'}
          {include file='catalog/_partials/product-cover-thumbnails.tpl'}
        </section>
      {/block}
    </div>

    <!-- Product Information -->
    <div class="col-md-6">
      <h1 class="h1">{$product.name}</h1>
      {include file='catalog/_partials/product-prices.tpl'}

      <div class="product-information">
        <div id="product-description-short-{$product.id}" class="product-description">{$product.description_short nofilter}</div>

        <!-- Product Customization -->
        {if $product.is_customizable && count($product.customizations.fields)}
          {include file="catalog/_partials/product-customization.tpl" customizations=$product.customizations}
        {/if}

        <!-- Add to Cart -->
        <div class="product-actions js-product-actions">
          <form action="{$urls.pages.cart}" method="post" id="add-to-cart-or-refresh">
            <input type="hidden" name="token" value="{$static_token}">
            <input type="hidden" name="id_product" value="{$product.id}" id="product_page_product_id">
            <input type="hidden" name="id_customization" value="{$product.id_customization}" id="product_customization_id">

            {include file='catalog/_partials/product-variants.tpl'}
            {include file='catalog/_partials/product-discounts.tpl'}
            {include file='catalog/_partials/product-add-to-cart.tpl'}
          </form>
        </div>

       
      </div>

      <!-- Tabs for Description and Details -->
      <div class="tabs">
        <ul class="nav nav-tabs" role="tablist">
          {if $product.description}
            <li class="nav-item">
              <a class="nav-link active" data-toggle="tab" href="#description" role="tab">{l s='Description' d='Shop.Theme.Catalog'}</a>
            </li>
          {/if}
          {if $product.attachments}
            <li class="nav-item">
              <a class="nav-link" data-toggle="tab" href="#attachments" role="tab">{l s='Attachments' d='Shop.Theme.Catalog'}</a>
            </li>
          {/if}
        </ul>

        <div class="tab-content">
          <div class="tab-pane fade show js-product-tab-active active in" id="description" role="tabpanel">
            <div class="product-description">{$product.description nofilter}</div>
          </div>
          <div class="tab-pane fade" id="product-details" role="tabpanel">
            {include file='catalog/_partials/product-details.tpl'}
          </div>
          {if $product.attachments}
            <div class="tab-pane fade" id="attachments" role="tabpanel">
              {foreach from=$product.attachments item=attachment}
                <div class="attachment">
                  <h4><a href="{url entity='attachment' params=['id_attachment' => $attachment.id_attachment]}">{$attachment.name}</a></h4>
                  <p>{$attachment.description}</p>
                </div>
              {/foreach}
            </div>
          {/if}
        </div>
      </div>

       <!-- Additional Info -->
        {include file='catalog/_partials/product-additional-info.tpl'}
        {hook h='displayReassurance'}
    </div>
  </div>
</section>
{/block}

{block name='scripts'}
  <script>
   window.onload = function() {
    $('#description').tab('show'); // Ustawienie zakładki "Opis" jako aktywnej
};

  </script>
{/block}
