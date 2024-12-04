{assign var=_counter value=0}
{function name="menu" nodes=[] depth=0 parent=null}
    {if $nodes|count}
      <ul class="top-menu" {if $depth == 0}id="top-menu"{/if} data-depth="{$depth}">
        {foreach from=$nodes item=node key=node_key}
            <li class="{$node.type}{if $node.current} current{/if}" id="{$node.page_identifier}">
              <a
                class="{if $depth >= 0}dropdown-item{/if}{if $depth === 1} dropdown-submenu{/if}"
                href="{$node.url}" data-depth="{$depth}"
                {if $node.open_in_new_window} target="_blank" {/if}
              >
                {if isset($node.image) && $node.image}
                  <div class="menu-image">
                    <img src="{$node.image}" alt="{$node.label}" class="menu-category-image"/>
                  </div>
                {/if}
                <span>
                  {$node.label}
                  {if $depth == 0 && $node.children|count} <!-- Strzałka tylko dla głównych kategorii -->
                    <i class="fas fa-chevron-down"></i> <!-- Ikona strzałki -->
                  {/if}
                  {if $depth == 1 && $node_key != count($nodes)-1} <!-- Separator tylko dla podkategorii -->
                        |<!-- Separator tylko w podkategoriach -->
                  {/if}
                </span>
              </a>

              {if $node.children|count}
                <div {if $depth === 0} class="popover sub-menu js-sub-menu collapse"{else} class="collapse"{/if} id="top_sub_menu_{$_counter}">
                  {menu nodes=$node.children depth=$node.depth parent=$node}
                </div>
              {/if}
            </li>

            

            {assign var=_counter value=$_counter+1} <!-- Zwiększenie licznika dla unikalnych ID -->
        {/foreach}
      </ul>
    {/if}
{/function}

<div class="menu js-top-menu position-static hidden-sm-down" id="_desktop_top_menu">
    {menu nodes=$menu.children}
    <div class="clearfix"></div>
</div>
