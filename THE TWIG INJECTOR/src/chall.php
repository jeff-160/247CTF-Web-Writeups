<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class ChallengeController extends AbstractController
{

    /**
     * @Route("/inject")
     */
    public function inject(Request $request)
    {
        $inject = preg_replace('/[^{\.}a-z\|\_]/', '', $request->query->get('inject'));
        $response = new Response($this->get('twig')->createTemplate("Welcome to the twig injector!\n${inject}")->render());
        $response->headers->set('Content-Type', 'text/plain');
        return $response;
    }

    /**
     * @Route("/")
     */
    public function index()
    {
        return new Response(highlight_file(__FILE__, true));
    }
}