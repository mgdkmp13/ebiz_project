<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Ps_LatestProducts extends Module
{
    public function __construct()
    {
        $this->name = 'ps_latestproducts';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'Twoja Nazwa';
        $this->need_instance = 0;
        $this->bootstrap = true;

        parent::__construct();

        $this->displayName = $this->l('Latest Products');
        $this->description = $this->l('Displays the latest 13 products on the homepage.');
    }

    public function install()
    {
        return parent::install() &&
            $this->registerHook('displayHome');
    }

    public function hookDisplayHome($params)
    {
        $products = $this->getLatestProducts(13);

        $this->context->smarty->assign([
            'latest_products' => $products,
        ]);

        return $this->display(__FILE__, 'views/templates/hook/latestproducts.tpl');
    }

    private function getLatestProducts($limit)
    {
        $sql = new DbQuery();
        $sql->select('*');
        $sql->from('product', 'p');
        $sql->where('p.active = 1');
        $sql->orderBy('p.date_add DESC');
        $sql->limit((int) $limit);

        $products = Db::getInstance()->executeS($sql);

        foreach ($products as &$product) {
            $product['link'] = $this->context->link->getProductLink((int)$product['id_product']);
            //$product['image'] = $this->context->link->getImageLink($product['link_rewrite'], $product['id_product']);
        }

        return $products;
    }
}
