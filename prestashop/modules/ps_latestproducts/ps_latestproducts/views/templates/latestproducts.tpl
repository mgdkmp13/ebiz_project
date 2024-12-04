<div class="latest-products">
    <h2>{l s='Latest Products'}</h2>
    <div class="products-list">
        {foreach from=$latest_products item=product}
            <div class="product">
                <a href="{$product.link}">
                    <img src="{$product.image}" alt="{$product.name}">
                    <h3>{$product.name|escape:'html':'UTF-8'}</h3>
                    <span class="price">{$product.price}</span>
                </a>
            </div>
        {/foreach}
    </div>
</div>
